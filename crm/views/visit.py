from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from crm.models.visit import SiteVisit
from crm.forms.other import SiteVisitForm


@login_required
def visit_list(request):
    user = request.user
    qs = SiteVisit.objects.select_related('lead', 'property', 'agent')

    if user.is_agent:
        qs = qs.filter(agent=user)

    status = request.GET.get('status')
    if status:
        qs = qs.filter(status=status)

    date = request.GET.get('date')
    if date:
        qs = qs.filter(scheduled_date=date)

    upcoming = qs.filter(scheduled_date__gte=timezone.now().date(), status='scheduled')
    past = qs.filter(scheduled_date__lt=timezone.now().date()).exclude(status='scheduled')

    context = {
        'visits': qs,
        'upcoming': upcoming[:10],
        'past': past[:10],
    }
    return render(request, 'crm/visit_list.html', context)


@login_required
def visit_create(request):
    if request.method == 'POST':
        form = SiteVisitForm(request.POST)
        if form.is_valid():
            visit = form.save()
            messages.success(request, f'Site visit {visit.visit_id} scheduled.')
            return redirect('visit_detail', pk=visit.pk)
    else:
        initial = {}
        lead_id = request.GET.get('lead')
        property_id = request.GET.get('property')
        if lead_id:
            initial['lead'] = lead_id
        if property_id:
            initial['property'] = property_id
        form = SiteVisitForm(initial=initial)
    return render(request, 'crm/visit_form.html', {'form': form, 'title': 'Schedule Visit'})


@login_required
def visit_detail(request, pk):
    visit = get_object_or_404(SiteVisit.objects.select_related('lead', 'property', 'agent'), pk=pk)

    if request.method == 'POST':
        visit.status = request.POST.get('status', visit.status)
        visit.feedback = request.POST.get('feedback', '')
        visit.lead_interested = request.POST.get('lead_interested')
        if visit.lead_interested == 'true':
            visit.lead_interested = True
        elif visit.lead_interested == 'false':
            visit.lead_interested = False
        else:
            visit.lead_interested = None
        visit.notes = request.POST.get('notes', visit.notes)
        visit.save()
        messages.success(request, 'Visit updated.')
        return redirect('visit_detail', pk=pk)

    return render(request, 'crm/visit_detail.html', {'visit': visit})


@login_required
def visit_cancel(request, pk):
    visit = get_object_or_404(SiteVisit, pk=pk)
    if request.method == 'POST':
        visit.status = 'cancelled'
        visit.save()
        messages.success(request, 'Visit cancelled.')
    return redirect('visit_list')

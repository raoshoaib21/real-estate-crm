from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from crm.models.lead import Lead
from crm.models.interaction import Interaction, Task
from crm.forms.lead import LeadForm
from crm.forms.other import InteractionForm, TaskForm


@login_required
def lead_list(request):
    user = request.user
    qs = Lead.objects.select_related('assigned_to').prefetch_related('interactions')

    if user.is_agent:
        qs = qs.filter(Q(assigned_to=user) | Q(assigned_to__isnull=True))

    search = request.GET.get('q')
    if search:
        qs = qs.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search) |
            Q(lead_id__icontains=search)
        )

    lead_type = request.GET.get('type')
    if lead_type:
        qs = qs.filter(lead_type=lead_type)

    status = request.GET.get('status')
    if status:
        qs = qs.filter(status=status)

    priority = request.GET.get('priority')
    if priority:
        qs = qs.filter(priority=priority)

    source = request.GET.get('source')
    if source:
        qs = qs.filter(source=source)

    assigned = request.GET.get('assigned')
    if assigned and not user.is_agent:
        qs = qs.filter(assigned_to_id=assigned)

    sort = request.GET.get('sort', '-created_at')
    qs = qs.order_by(sort)

    paginator = Paginator(qs, 20)
    page = request.GET.get('page')
    leads = paginator.get_page(page)

    agents = user.is_manager and None or []

    context = {
        'leads': leads,
        'agents': agents,
    }
    return render(request, 'crm/lead_list.html', context)


@login_required
def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            messages.success(request, f'Lead {lead.lead_id} created successfully.')
            return redirect('lead_detail', pk=lead.pk)
    else:
        form = LeadForm()
    return render(request, 'crm/lead_form.html', {'form': form, 'title': 'Add Lead'})


@login_required
def lead_detail(request, pk):
    lead = get_object_or_404(Lead.objects.select_related('assigned_to'), pk=pk)
    interactions = lead.interactions.select_related('created_by')[:20]
    tasks = lead.tasks.select_related('assigned_to')
    visits = lead.visits.select_related('property', 'agent')[:10]
    deals = lead.deals.select_related('deal_property', 'agent', 'stage')

    if request.method == 'POST':
        if 'interaction_submit' in request.POST:
            int_form = InteractionForm(request.POST)
            if int_form.is_valid():
                interaction = int_form.save(commit=False)
                interaction.lead = lead
                interaction.created_by = request.user
                interaction.save()
                lead.last_contacted = interaction.created_at
                lead.save()
                messages.success(request, 'Interaction logged.')
                return redirect('lead_detail', pk=pk)
        elif 'task_submit' in request.POST:
            task_form = TaskForm(request.POST)
            if task_form.is_valid():
                task = task_form.save(commit=False)
                task.related_lead = lead
                task.save()
                messages.success(request, 'Task created.')
                return redirect('lead_detail', pk=pk)
    else:
        int_form = InteractionForm()
        task_form = TaskForm(initial={'assigned_to': lead.assigned_to})

    context = {
        'lead': lead,
        'interactions': interactions,
        'tasks': tasks,
        'visits': visits,
        'deals': deals,
        'int_form': int_form,
        'task_form': task_form,
    }
    return render(request, 'crm/lead_detail.html', context)


@login_required
def lead_edit(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead updated.')
            return redirect('lead_detail', pk=pk)
    else:
        form = LeadForm(instance=lead)
    return render(request, 'crm/lead_form.html', {'form': form, 'title': 'Edit Lead', 'lead': lead})


@login_required
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        lead.delete()
        messages.success(request, 'Lead deleted.')
        return redirect('lead_list')
    return render(request, 'crm/lead_confirm_delete.html', {'lead': lead})


@login_required
def lead_status_update(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            lead.status = new_status
            lead.save()
            messages.success(request, f'Lead status updated to {lead.get_status_display()}.')
    return redirect('lead_detail', pk=pk)

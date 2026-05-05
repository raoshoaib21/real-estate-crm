from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from crm.models.deal import Deal, PipelineStage, DealActivity
from crm.forms.other import DealForm, DealActivityForm


@login_required
def deal_list(request):
    user = request.user
    qs = Deal.objects.select_related('lead', 'deal_property', 'agent', 'stage')

    if user.is_agent:
        qs = qs.filter(agent=user)

    search = request.GET.get('q')
    if search:
        qs = qs.filter(
            lead__first_name__icontains=search
        ) | qs.filter(
            lead__last_name__icontains=search
        ) | qs.filter(
            deal_id__icontains=search
        )

    stage = request.GET.get('stage')
    if stage:
        qs = qs.filter(stage_id=stage)

    sort = request.GET.get('sort', '-created_at')
    qs = qs.order_by(sort)

    stages = PipelineStage.objects.all()
    deals = qs

    context = {
        'deals': deals,
        'stages': stages,
    }
    return render(request, 'crm/deal_list.html', context)


@login_required
def pipeline_board(request):
    user = request.user
    qs = Deal.objects.select_related('lead', 'deal_property', 'agent', 'stage')

    if user.is_agent:
        qs = qs.filter(agent=user)

    stages = PipelineStage.objects.all()
    stage_data = []

    for stage in stages:
        stage_deals = qs.filter(stage=stage)
        total_value = stage_deals.aggregate(total=Sum('deal_value'))['total'] or 0
        stage_data.append({
            'stage': stage,
            'deals': stage_deals,
            'count': stage_deals.count(),
            'total_value': total_value,
        })

    context = {
        'stage_data': stage_data,
    }
    return render(request, 'crm/pipeline_board.html', context)


@login_required
def deal_create(request):
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            deal = form.save(commit=False)
            deal.agent = deal.agent or request.user
            deal.save()
            messages.success(request, f'Deal {deal.deal_id} created.')
            return redirect('deal_detail', pk=deal.pk)
    else:
        initial = {}
        lead_id = request.GET.get('lead')
        property_id = request.GET.get('property')
        if lead_id:
            initial['lead'] = lead_id
        if property_id:
            initial['property'] = property_id
        form = DealForm(initial=initial)
    return render(request, 'crm/deal_form.html', {'form': form, 'title': 'Create Deal'})


@login_required
def deal_detail(request, pk):
    deal = get_object_or_404(Deal.objects.select_related('lead', 'deal_property', 'agent', 'stage'), pk=pk)
    activities = deal.activities.select_related('created_by')

    if request.method == 'POST':
        activity_form = DealActivityForm(request.POST)
        if activity_form.is_valid():
            activity = activity_form.save(commit=False)
            activity.deal = deal
            activity.created_by = request.user
            activity.save()
            messages.success(request, 'Activity logged.')
            return redirect('deal_detail', pk=pk)
    else:
        activity_form = DealActivityForm()

    context = {
        'deal': deal,
        'activities': activities,
        'activity_form': activity_form,
    }
    return render(request, 'crm/deal_detail.html', context)


@login_required
def deal_edit(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    if request.method == 'POST':
        form = DealForm(request.POST, instance=deal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deal updated.')
            return redirect('deal_detail', pk=pk)
    else:
        form = DealForm(instance=deal)
    return render(request, 'crm/deal_form.html', {'form': form, 'title': 'Edit Deal', 'deal': deal})


@login_required
def deal_stage_update(request):
    if request.method == 'POST':
        deal_id = request.POST.get('deal_id')
        stage_id = request.POST.get('stage_id')
        deal = get_object_or_404(Deal, pk=deal_id)
        new_stage = get_object_or_404(PipelineStage, pk=stage_id)

        old_stage = deal.stage
        deal.stage = new_stage
        deal.save()

        DealActivity.objects.create(
            deal=deal,
            activity_type='note',
            description=f"Stage changed from '{old_stage.name}' to '{new_stage.name}'",
            created_by=request.user,
        )

        return JsonResponse({'status': 'ok', 'deal_id': deal.deal_id, 'stage': new_stage.name})
    return JsonResponse({'status': 'error'}, status=400)

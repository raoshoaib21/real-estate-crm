from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from crm.models.commission import Commission
from crm.models.deal import Deal
from crm.models.user import CustomUser
from crm.forms.other import CommissionForm


@login_required
def commission_list(request):
    user = request.user
    qs = Commission.objects.select_related('deal', 'agent', 'split_with')

    if user.is_agent:
        qs = qs.filter(agent=user)

    status = request.GET.get('status')
    if status:
        qs = qs.filter(status=status)

    agent = request.GET.get('agent')
    if agent and user.is_manager:
        qs = qs.filter(agent_id=agent)

    total_pending = qs.filter(status='pending').aggregate(total=Sum('net_amount'))['total'] or 0
    total_paid = qs.filter(status='paid').aggregate(total=Sum('net_amount'))['total'] or 0

    commissions = qs.order_by('-created_at')

    agents = CustomUser.objects.filter(role='agent')

    context = {
        'commissions': commissions,
        'total_pending': total_pending,
        'total_paid': total_paid,
        'agents': agents,
    }
    return render(request, 'crm/commission_list.html', context)


@login_required
def commission_create(request):
    if request.method == 'POST':
        form = CommissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Commission record created.')
            return redirect('commission_list')
    else:
        form = CommissionForm()
    return render(request, 'crm/commission_form.html', {'form': form, 'title': 'Add Commission'})


@login_required
def commission_reports(request):
    user = request.user
    qs = Commission.objects.select_related('agent')

    if user.is_agent:
        qs = qs.filter(agent=user)

    total_earned = qs.filter(status='paid').aggregate(total=Sum('net_amount'))['total'] or 0
    total_pending = qs.filter(status='pending').aggregate(total=Sum('net_amount'))['total'] or 0
    total_deals = qs.aggregate(count=Count('id'))['count']

    agent_performance = []
    agents = CustomUser.objects.filter(role='agent')
    for agent in agents:
        agent_commissions = qs.filter(agent=agent)
        earned = agent_commissions.filter(status='paid').aggregate(total=Sum('net_amount'))['total'] or 0
        closed = Deal.objects.filter(agent=agent, stage__name='Closed').count()
        agent_performance.append({
            'agent': agent,
            'earned': earned,
            'deals_closed': closed,
            'pending': agent_commissions.filter(status='pending').aggregate(total=Sum('net_amount'))['total'] or 0,
        })

    agent_performance.sort(key=lambda x: x['earned'], reverse=True)

    monthly_data = []
    for month in range(1, 13):
        month_total = qs.filter(
            status='paid',
            paid_date__month=month,
            paid_date__year=timezone.now().year
        ).aggregate(total=Sum('net_amount'))['total'] or 0
        monthly_data.append({'month': month, 'total': float(month_total)})

    context = {
        'total_earned': total_earned,
        'total_pending': total_pending,
        'total_deals': total_deals,
        'agent_performance': agent_performance,
        'monthly_data': monthly_data,
    }
    return render(request, 'crm/commission_reports.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta
from crm.models.lead import Lead
from crm.models.property import Property
from crm.models.deal import Deal
from crm.models.visit import SiteVisit
from crm.models.commission import Commission
from crm.models.interaction import Task


@login_required
def dashboard(request):
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    user = request.user

    if user.is_agent:
        leads = Lead.objects.filter(assigned_to=user)
        deals = Deal.objects.filter(agent=user)
        properties = Property.objects.filter(listed_by=user)
        visits = SiteVisit.objects.filter(agent=user)
        tasks = Task.objects.filter(assigned_to=user)
        commissions = Commission.objects.filter(agent=user)
    else:
        leads = Lead.objects.all()
        deals = Deal.objects.all()
        properties = Property.objects.all()
        visits = SiteVisit.objects.all()
        tasks = Task.objects.all()
        commissions = Commission.objects.all()

    today_visits = visits.filter(scheduled_date=today)
    pending_tasks = tasks.filter(status__in=['pending', 'in_progress'])
    overdue_tasks = tasks.filter(status='overdue') | tasks.filter(due_date__lt=today, status__in=['pending', 'in_progress'])

    total_pipeline_value = deals.exclude(stage__name__in=['Closed', 'Lost']).aggregate(total=Sum('deal_value'))['total'] or 0
    monthly_commissions = commissions.filter(
        status='paid',
        paid_date__month=today.month,
        paid_date__year=today.year
    ).aggregate(total=Sum('net_amount'))['total'] or 0

    lead_stats = leads.values('status').annotate(count=Count('id')).order_by()
    deal_stats = deals.values('stage__name').annotate(count=Count('id'), total_value=Sum('deal_value')).order_by()

    recent_leads = leads.select_related('assigned_to')[:10]
    recent_deals = deals.select_related('lead', 'property', 'agent')[:5]

    conversion_data = []
    statuses = ['new', 'contacted', 'qualified', 'proposal', 'negotiation', 'won', 'lost']
    for status in statuses:
        count = leads.filter(status=status).count()
        conversion_data.append({'status': status, 'count': count})

    context = {
        'total_leads': leads.count(),
        'total_properties': properties.count(),
        'active_deals': deals.exclude(stage__name__in=['Closed', 'Lost']).count(),
        'closed_deals': deals.filter(stage__name='Closed').count(),
        'today_visits': today_visits,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks.count(),
        'total_pipeline_value': total_pipeline_value,
        'monthly_commissions': monthly_commissions,
        'lead_stats': lead_stats,
        'deal_stats': deal_stats,
        'recent_leads': recent_leads,
        'recent_deals': recent_deals,
        'conversion_data': conversion_data,
    }

    return render(request, 'crm/dashboard.html', context)

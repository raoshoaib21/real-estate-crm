from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from crm.models.lead import Lead
from crm.models.property import Property
from crm.models.deal import Deal
from crm.models.visit import SiteVisit
from crm.models.commission import Commission
from crm.models.user import CustomUser


@login_required
def reports(request):
    user = request.user
    lead_qs = Lead.objects.all() if user.is_manager else Lead.objects.filter(assigned_to=user)
    deal_qs = Deal.objects.all() if user.is_manager else Deal.objects.filter(agent=user)
    property_qs = Property.objects.all() if user.is_manager else Property.objects.filter(listed_by=user)

    lead_source_data = []
    for source_code, source_name in Lead.SOURCE_CHOICES:
        count = lead_qs.filter(source=source_code).count()
        if count > 0:
            lead_source_data.append({'source': source_name, 'count': count})

    lead_type_data = []
    for type_code, type_name in Lead.TYPE_CHOICES:
        count = lead_qs.filter(lead_type=type_code).count()
        lead_type_data.append({'type': type_name, 'count': count})

    property_type_data = []
    for type_code, type_name in Property.PROPERTY_TYPES:
        count = property_qs.filter(property_type=type_code).count()
        avg_price = property_qs.filter(property_type=type_code).aggregate(avg=Avg('price'))['avg']
        if count > 0:
            property_type_data.append({'type': type_name, 'count': count, 'avg_price': float(avg_price or 0)})

    deal_stage_data = []
    for deal in deal_qs.select_related('stage'):
        deal_stage_data.append({
            'stage': deal.stage.name if deal.stage else 'Unknown',
            'value': float(deal.deal_value),
            'probability': deal.probability,
        })

    conversion_rates = []
    total_leads = lead_qs.count()
    for status_code, status_name in Lead.STATUS_CHOICES:
        count = lead_qs.filter(status=status_code).count()
        rate = (count / total_leads * 100) if total_leads > 0 else 0
        conversion_rates.append({
            'status': status_name,
            'count': count,
            'rate': round(rate, 1),
        })

    context = {
        'lead_source_data': lead_source_data,
        'lead_type_data': lead_type_data,
        'property_type_data': property_type_data,
        'deal_stage_data': deal_stage_data,
        'conversion_rates': conversion_rates,
        'total_leads': total_leads,
        'total_deals': deal_qs.count(),
        'total_properties': property_qs.count(),
    }
    return render(request, 'crm/reports.html', context)

from crm.views.dashboard import dashboard
from crm.views.property import property_list, property_create, property_detail, property_edit, property_delete, property_add_image
from crm.views.lead import lead_list, lead_create, lead_detail, lead_edit, lead_delete, lead_status_update
from crm.views.deal import deal_list, pipeline_board, deal_create, deal_detail, deal_edit, deal_stage_update
from crm.views.visit import visit_list, visit_create, visit_detail, visit_cancel
from crm.views.commission import commission_list, commission_create, commission_reports
from crm.views.reports import reports

__all__ = [
    'dashboard',
    'property_list', 'property_create', 'property_detail', 'property_edit', 'property_delete', 'property_add_image',
    'lead_list', 'lead_create', 'lead_detail', 'lead_edit', 'lead_delete', 'lead_status_update',
    'deal_list', 'pipeline_board', 'deal_create', 'deal_detail', 'deal_edit', 'deal_stage_update',
    'visit_list', 'visit_create', 'visit_detail', 'visit_cancel',
    'commission_list', 'commission_create', 'commission_reports',
    'reports',
]

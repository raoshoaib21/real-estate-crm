from crm.models.user import CustomUser
from crm.models.property import Property, PropertyImage, PropertyDocument
from crm.models.lead import Lead, LeadSource
from crm.models.deal import Deal, PipelineStage, DealActivity
from crm.models.visit import SiteVisit
from crm.models.commission import Commission
from crm.models.interaction import Interaction, Task

__all__ = [
    'CustomUser',
    'Property', 'PropertyImage', 'PropertyDocument',
    'Lead', 'LeadSource',
    'Deal', 'PipelineStage', 'DealActivity',
    'SiteVisit',
    'Commission',
    'Interaction', 'Task',
]

from crm.forms.user import CustomUserCreationForm, CustomUserChangeForm, AgentProfileForm
from crm.forms.property import PropertyForm, PropertyImageForm
from crm.forms.lead import LeadForm, LeadQuickForm
from crm.forms.other import (
    DealForm, DealActivityForm, SiteVisitForm,
    CommissionForm, InteractionForm, TaskForm,
)

__all__ = [
    'CustomUserCreationForm', 'CustomUserChangeForm', 'AgentProfileForm',
    'PropertyForm', 'PropertyImageForm',
    'LeadForm', 'LeadQuickForm',
    'DealForm', 'DealActivityForm', 'SiteVisitForm',
    'CommissionForm', 'InteractionForm', 'TaskForm',
]

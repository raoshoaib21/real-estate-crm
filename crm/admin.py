from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from crm.models.user import CustomUser
from crm.models.property import Property, PropertyImage
from crm.models.lead import Lead, LeadSource
from crm.models.deal import Deal, PipelineStage, DealActivity
from crm.models.visit import SiteVisit
from crm.models.commission import Commission
from crm.models.interaction import Interaction, Task


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('CRM Info', {'fields': ('role', 'phone', 'profile_photo', 'license_number', 'commission_rate')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('CRM Info', {'fields': ('role', 'phone', 'commission_rate')}),
    )


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['listing_id', 'title', 'property_type', 'status', 'price', 'city', 'listed_by']
    list_filter = ['property_type', 'status', 'city', 'featured']
    search_fields = ['title', 'listing_id', 'address', 'city']


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['lead_id', 'full_name', 'lead_type', 'status', 'priority', 'assigned_to', 'lead_score']
    list_filter = ['lead_type', 'status', 'priority', 'source']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'lead_id']


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['deal_id', 'lead', 'deal_property', 'stage', 'deal_value', 'agent']
    list_filter = ['stage', 'deal_type']


@admin.register(PipelineStage)
class PipelineStageAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'probability']
    ordering = ['order']


@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ['visit_id', 'lead', 'property', 'scheduled_date', 'status']
    list_filter = ['status']


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ['agent', 'deal', 'commission_amount', 'net_amount', 'status']
    list_filter = ['status']


admin.site.register(Interaction)
admin.site.register(Task)
admin.site.register(PropertyImage)
admin.site.register(DealActivity)
admin.site.register(LeadSource)

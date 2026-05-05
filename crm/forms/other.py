from django import forms
from crm.models.deal import Deal, DealActivity
from crm.models.visit import SiteVisit
from crm.models.commission import Commission
from crm.models.interaction import Interaction, Task


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = [
            'lead', 'deal_property', 'agent', 'stage', 'deal_value',
            'offer_amount', 'counter_offer', 'deal_type',
            'expected_close_date', 'notes',
        ]
        widgets = {
            'expected_close_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'})


class DealActivityForm(forms.ModelForm):
    class Meta:
        model = DealActivity
        fields = ['activity_type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class SiteVisitForm(forms.ModelForm):
    class Meta:
        model = SiteVisit
        fields = ['lead', 'property', 'agent', 'scheduled_date', 'scheduled_time', 'notes']
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
            'scheduled_time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'})


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['deal', 'agent', 'commission_rate', 'split_with', 'split_percentage', 'status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'})


class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['interaction_type', 'subject', 'description', 'follow_up_date']
        widgets = {
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'related_lead', 'due_date', 'priority']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

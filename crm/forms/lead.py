from django import forms
from crm.models.lead import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'lead_type', 'first_name', 'last_name', 'email', 'phone', 'source',
            'status', 'assigned_to', 'priority', 'budget_min', 'budget_max',
            'expected_sell_price', 'preferred_location', 'preferred_type',
            'requirements', 'notes',
        ]
        widgets = {
            'requirements': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'})


class LeadQuickForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['first_name', 'last_name', 'email', 'phone', 'lead_type', 'budget_max']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'})

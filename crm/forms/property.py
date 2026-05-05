from django import forms
from crm.models.property import Property, PropertyImage


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'property_type', 'status', 'price', 'negotiable',
            'area_sqft', 'bedrooms', 'bathrooms', 'address', 'city', 'state',
            'zip_code', 'country', 'year_built', 'floor', 'total_floors',
            'parking_spaces', 'featured',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'})


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'is_primary', 'caption']

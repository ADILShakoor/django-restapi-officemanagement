from django import forms
from .models import Asset,AssertCategory

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'name',
            'category',
            'status',
            # 'company',
            'assigned_to',
            'serial_number',
            'purchase_date',
            'value',
            'maintenance_date',
            'description',
        ]
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'maintenance_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AssertCategoryForm(forms.ModelForm):
    class Meta:
        model=AssertCategory
        fields=[
            'name',
            'description',
        ]
    
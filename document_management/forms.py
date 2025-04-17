from django import forms
from .models import EmployeeDocument

class EmployeeDocumentForm(forms.ModelForm):
    class Meta:
        model = EmployeeDocument
        fields = ["employee",'document_type', 'title', 'file', 'expires_on', 'signature_link', 'notes']
        widgets = {
            'expires_on': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

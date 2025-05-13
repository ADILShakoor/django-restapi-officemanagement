from django import forms
from .models import JobApplication,Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'last_date_to_apply']
        widgets = {
            'last_date_to_apply': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['name', 'email', 'phone', 'address', 'experience_years', 'company', 'cover_letter', 'resume']

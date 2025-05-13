from django import forms
from .models import CalendarEvent
from django.core.exceptions import ValidationError

class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['title','event_type',"project", 'description', 'location', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
        def clean(self):
           cleaned_data = super().clean()
           start_time = cleaned_data.get("start_time")
           end_time = cleaned_data.get("end_time")
   
           if start_time and end_time and start_time > end_time:
              raise ValidationError("Start time must be before end time.")

from django import forms
from .models import Project
from my_app.models import CustomUser
from .models import Task

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
        
# class AssignEmployeesForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         fields = ['assigned_employees']
        
class AssignEmployeeForm(forms.Form):
    employee = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='employee', assigned_projects=None), 
        empty_label="Select Employee"
    )



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'assigned_to', 'status', 'weight', 'due_date', 'image']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)  # Get project from view
        super(TaskForm, self).__init__(*args, **kwargs)
        if project:
            self.fields['assigned_to'].queryset = project.assigned_employees.all()
class TaskRemarkform(forms.ModelForm):
    class Meta:
        model=Task
        fields=['status']
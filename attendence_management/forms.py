from django import forms
from .models import Attendance, LeaveApplication, WorkShift, EmployeeShift , LeaveType

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['status', 'clock_in', 'clock_out', 'remarks']

    def clean(self): 
        cleaned_data = super().clean()
        clock_in = cleaned_data.get('clock_in')
        clock_out = cleaned_data.get('clock_out')

        if clock_in and clock_out and clock_out <= clock_in:
            raise forms.ValidationError("Clock-out time must be after clock-in time.")

        return cleaned_data


class LeaveApplicationForm(forms.ModelForm):
    # start_date=forms.DateField(placeholder="YYYY-MM-DD")
    status=forms.CharField(max_length=20, required=False)
    
    class Meta:
        model = LeaveApplication
        fields = ['leave_type', 'start_date', 'end_date','status', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
             'end_date': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}), 
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date must be after start date.")

        return cleaned_data

class LeaveApplicationApprovalForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ['status']  

class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model=LeaveType 
        fields=["name","description"]



class WorkShiftForm(forms.ModelForm):
    class Meta:
        model = WorkShift
        fields = ['name', 'start_time', 'end_time']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and end_time <= start_time:
            raise forms.ValidationError("Shift end time must be after start time.")

        return cleaned_data



class EmployeeShiftForm(forms.ModelForm):
    class Meta:
        model = EmployeeShift
        fields = ['employee', 'shift']


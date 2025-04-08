from django.db import models

# Create your models here.
from django.db import models
from my_app.models import CustomUser, Company  # Import User & Company
 
# Attendance Model
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('on_leave', 'On Leave'),
    ]
    
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="attendances")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Each employee belongs to a company
    date = models.DateField(auto_now_add=True)  # Auto-set when attendance is marked
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    clock_in = models.TimeField(null=True, blank=True)
    clock_out = models.TimeField(null=True, blank=True)
    overtime_hours = models.FloatField(default=0.0)  # Extra work hours
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('employee', 'date')  # Ensure one record per employee per day

    def __str__(self):
        return f"{self.employee.username} - {self.date} - {self.status}"

# Leave Type Model
class LeaveType(models.Model):
    name = models.CharField(max_length=100, unique=True)  # E.g., "Sick Leave", "Casual Leave"
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Leave Application Model
class LeaveApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'), 
    ] 
    
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="leave_requests")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)  # When the leave was applied
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_leaves")

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type.name} - {self.status}"

# Work Shift Model
class WorkShift(models.Model):
    SHIFT_CHOICES = [
        ('morning', 'Morning Shift'),
        ('evening', 'Evening Shift'),
        ('night', 'Night Shift'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, choices=SHIFT_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.company.name} - {self.name} ({self.start_time} to {self.end_time})"

# Assign Employee to Work Shift
class EmployeeShift(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="assigned_shifts")
    shift = models.ForeignKey(WorkShift, on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} - {self.shift.name} ({self.assigned_date})"

from django.contrib import admin
from .models import Attendance,LeaveApplication,LeaveType,WorkShift,EmployeeShift
# Register your models here.
admin.site.register(Attendance)
admin.site.register(LeaveType)
admin.site.register(LeaveApplication)
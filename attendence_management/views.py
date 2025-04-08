from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Attendance, LeaveApplication, WorkShift, EmployeeShift
from .forms import AttendanceForm, LeaveApplicationForm, WorkShiftForm, EmployeeShiftForm,LeaveTypeForm,LeaveApplicationApprovalForm



@login_required
def attendance_list(request):
    user = request.user
    # if user.role == 'super_admin':
    attendances = Attendance.objects.filter(company=user.company)
    # elif user.role == 'admin':
    #     attendances = Attendance.objects.filter(employee__company=user.company)
    # elif user.role == 'team_lead':
    #     attendances = Attendance.objects.filter(employee__company=user.company, employee__role='employee')
    # else:
    #     attendances = Attendance.objects.filter(employee=user)
    
    return render(request, 'attendance_management/attendance_list.html', {'attendances': attendances})

@login_required
def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendence=form.save(commit=False)
            attendence.employee=request.user
            attendence.company=request.user.company
            attendence.save()
            return redirect('view_self_attendances')  
    else:
        form = AttendanceForm()
    return render(request, 'attendance_management/attendance_form.html', {'form': form})

@login_required
def attendance_update(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('attendance-list')
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'attendance_management/attendance_form.html', {'form': form})

@login_required
def attendance_delete(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        return redirect('attendance-list')
    return render(request, 'attendance_management/attendance_confirm_delete.html', {'attendance': attendance})


@login_required 
def leave_list(request):
    leaves = LeaveApplication.objects.all()
    return render(request, 'attendance_management/leave_application_list.html', {'leaves': leaves})
 
@login_required
def leave_create(request):
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave=form.save(commit=False)
            leave.company=request.user.company
            leave.employee=request.user
            leave.status="pending"
            leave.save()
            return redirect('view_self_leaves')   
    else:
        form = LeaveApplicationForm()
    return render(request, 'attendance_management/leave_application_form.html', {'form': form})

@login_required
def leave_update(request, pk):
    leave = get_object_or_404(LeaveApplication, pk=pk)
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST, instance=leave)
        if form.is_valid():
            leave=form.save(commit=False)
            # leave.company=request.user.company
            # leave.employee=request.user
            leave.status='pending' 
            leave.save()
            return redirect('leave-application-list')
        else:
            print(form.errors)
    else:
        form = LeaveApplicationForm(instance=leave)
    return render(request, 'attendance_management/leave_application_form.html', {'form': form})

def leave_approval(request, pk):
    user = request.user
    approval = get_object_or_404(LeaveApplication, pk=pk)

    if user.role in ["team_lead", "ceo"]: 
        if request.method == "POST":
            form = LeaveApplicationApprovalForm(request.POST, instance=approval)
            if form.is_valid():
                form.save()  
                return redirect("leave-application-list") 
            else:
                print(form.errors) 
        else:
            form = LeaveApplicationApprovalForm(instance=approval)  
    else:
        return HttpResponse("You are not allowed to perform this action.") 

    return render(request, 'attendance_management/leave_aproval.html', {'form': form})
        

def add_leave_categorey(request):
    if request.method=="POST":
        form=LeaveTypeForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect("leave-application-list")
    else:
        form=LeaveTypeForm()
    return render(request,"attendance_management/leave_categorey.html",{'form':form})
        
        

@login_required
def leave_delete(request, pk):
    leave = get_object_or_404(LeaveApplication, pk=pk)
    if request.method == 'POST':
        leave.delete()
        return redirect('leave-application-list')
    return render(request, 'attendance_management/leave_application_confirm_delete.html', {'leave': leave})



@login_required
def shift_list(request):
    shifts = WorkShift.objects.all()
    return render(request, 'attendance_management/shift_list.html', {'shifts': shifts})

@login_required
def shift_create(request):
    if request.method == 'POST':
        form = WorkShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shift-list')
    else:
        form = WorkShiftForm()
    return render(request, 'attendance_management/shift_form.html', {'form': form})

@login_required
def shift_update(request, pk):
    shift = get_object_or_404(WorkShift, pk=pk)
    if request.method == 'POST':
        form = WorkShiftForm(request.POST, instance=shift)
        if form.is_valid():
            form.save()
            return redirect('shift-list')
    else:
        form = WorkShiftForm(instance=shift)
    return render(request, 'attendance_management/shift_form.html', {'form': form})

@login_required
def shift_delete(request, pk):
    shift = get_object_or_404(WorkShift, pk=pk)
    if request.method == 'POST':
        shift.delete()
        return redirect('shift-list')
    return render(request, 'attendance_management/shift_confirm_delete.html', {'shift': shift})



@login_required
def employee_shift_list(request):
    employee_shifts = EmployeeShift.objects.all()
    return render(request, 'attendance_management/employee_shift_list.html', {'employee_shifts': employee_shifts})

@login_required
def employee_shift_create(request):
    if request.method == 'POST':
        form = EmployeeShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee-shift-list')
    else:
        form = EmployeeShiftForm()
    return render(request, 'attendance_management/employee_shift_form.html', {'form': form})

@login_required
def employee_shift_update(request, pk):
    employee_shift = get_object_or_404(EmployeeShift, pk=pk)
    if request.method == 'POST':
        form = EmployeeShiftForm(request.POST, instance=employee_shift)
        if form.is_valid():
            form.save()
            return redirect('employee-shift-list')
    else:
        form = EmployeeShiftForm(instance=employee_shift)
    return render(request, 'attendance_management/employee_shift_form.html', {'form': form})

@login_required
def employee_shift_delete(request, pk):
    employee_shift = get_object_or_404(EmployeeShift, pk=pk)
    if request.method == 'POST':
        employee_shift.delete()
        return redirect('employee-shift-list')
    return render(request, 'attendance_management/employee_shift_confirm_delete.html', {'employee_shift': employee_shift})

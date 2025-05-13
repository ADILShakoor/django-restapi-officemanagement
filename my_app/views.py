from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import CustomUser,Company
from my_asset.models import Asset
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from .forms import SimpleLoginForm
# from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm ,CustomUserChangeForm 
from project_management.models import Project,Task
from datetime import date
from attendence_management.models import Attendance,LeaveType,LeaveApplication
from document_management.models import EmployeeDocument
from google_calendar.models import CalendarEvent

# Helper Functions

def login_view(request):
    if request.method == 'POST':
        form = SimpleLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role != 'employee':
                    return redirect("home")
                # elif user.role == 'ceo':
                #     return redirect('manage_company_records')
                # elif user.role == 'team_lead':
                #     return redirect('manage_team_records')
                else:
                    return redirect('view_self_record')
                
            else:
                form.add_error(None,"Invalid username or password.")
    else:
        form = SimpleLoginForm()
    return render(request, 'login.html', {'form': form})
    
def is_admin(user):
    return user.is_superuser or user.role == 'admin'

def is_ceo(user):
    return user.role == 'ceo'

def is_team_lead(user):
    return user.role == 'team_lead'

def is_employee(user):
    return user.role == 'employee'

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def self_document(request):
    # print(request.user)
    documents = EmployeeDocument.objects.filter(employee=request.user)
    # print(documents)
    return render(request, 'dashboard/self_document.html', {'documents': documents})

@login_required
def self_document_detail(request, pk):
    document = get_object_or_404(EmployeeDocument, pk=pk, company=request.user.company)
    return render(request, 'dashboard/self_document_detail.html', {'document': document})


def can_manage_user(request_user, target_user):
    
    if request_user.role == 'admin':
        return True  
    elif request_user.role == 'ceo':
        return target_user.role in ['team_lead', 'employee'] and request_user.company == target_user.company
    elif request_user.role == 'team_lead':
        return target_user.role == 'employee' and request_user.company == target_user.company
    return False

@login_required
# @user_passes_test(lambda user: is_admin(user) or is_ceo(user))
def manage_company_records(request):
    if request.user.is_superuser:
       users = CustomUser.objects.all()
    if request.user.role == 'admin':
        users = CustomUser.objects.filter(company=request.user.company)  # Admin can see all users
    elif request.user.role == 'ceo':
        users = CustomUser.objects.filter(company=request.user.company, role__in=['team_lead', 'employee'])
    elif request.user.role == 'team_lead':
        users = CustomUser.objects.filter(company=request.user.company, role='employee')
    else:
        return render(request, '403.html') 
    # if request.user.is_superuser:
    #     records = CustomUser.objects.all()  # Superuser can view all records
    # if request.user.role=="ceo":
    #     records = CustomUser.objects.filter(company=request.user.company)  # CEO can view their company records

    return render(request, 'company_records.html', {'records': users})

# Team Lead View for Employee Records
@login_required
# @user_passes_test(is_team_lead)
def manage_team_records(request):
    if request.user.role not in ['ceo', 'team_lead']:
        return render(request,'403.html') 
    records = CustomUser.objects.filter(company=request.user.company, role='employee')
    return render(request, 'team_records.html', {'records': records})


# Employee View for Their Own Record

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def view_self_asset(request):
    assets=Asset.objects.filter(assigned_to=request.user.id)
    context={
        'assets':assets
        }
    return render(request, 'dashboard/self_asset.html',context)

def view_self_taskes(request):
    project_qs = Project.objects.filter(assigned_employees=request.user)
    # print(project_qs)
    meetings_qs = CalendarEvent.objects.filter(project__in=project_qs)
    taskes = Task.objects.filter(project__in=project_qs)  
    # user_project=get_object_or_404(project,project=project)
    # print(user_project)
    # taskes=Task.objects.filter(project=project)  
    context={
        'taskes':taskes,
        "meetings":meetings_qs, 
        }          
    return render(request, 'dashboard/self_taskes.html',context)

def view_self_attendances(request):
    attendances=Attendance.objects.filter(employee=request.user.id)
    context={
        'attendances':attendances
        }
    return render(request, 'dashboard/self_attendances.html',context)

def view_self_leaves(request):
    leaves=LeaveApplication.objects.filter(employee=request.user.id)
    context={
        "leaves":leaves,
        }
    return render(request, 'dashboard/self_leaves.html',context)

def view_self_projects(request):
    if request.user.role == 'team_lead':
        projects = Project.objects.filter(created_by=request.user)
    else:
       projects = Project.objects.filter(assigned_employees=request.user)
    context={
        "projects":projects,
        }
    return render(request, 'dashboard/self_projects.html',context)


@login_required
# @user_passes_test(is_employee)
def view_self_record(request):
    record = get_object_or_404(CustomUser, id=request.user.id)
    # assets=Asset.objects.filter(assigned_to=request.user.id)
    # taskes=Task.objects.filter(assigned_to=request.user)
    total_days=(date.today() - record.date_joined.date()).days
    # attendances=Attendance.objects.filter(employee=request.user.id)
    # leaves=LeaveApplication.objects.filter(employee=request.user.id)
    # projects = Project.objects.filter(
    #     created_by=request.user if request.user.role == 'team_lead' else None
    # ) or Project.objects.filter(assigned_employees=request.user)
    
    # join
    # if not assets.exists():
    #     message={
    #         "message":"NO asset is assigned to you"
    #     }
    # print(request.user)
    # if request.user.role == 'team_lead':
    #     projects = Project.objects.filter(created_by=request.user)
    # else:
    #    projects = Project.objects.filter(assigned_employees=request.user)
    # if not projects.exists():
    #     message={
    #         "message":"No Project is assigned to you"
    #     }
    context={
        "total_days":total_days,'record': record,
        # 'assets':assets,"projects":projects,
        # 'taskes':taskes,'attendances':attendances,
        # "leaves":leaves,
        }
    return render(request, 'self_record.html',context)



# Account Creation View
def create_account(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'create_account.html', {'form': form}) 

def edit_user(request, user_id):
    user = get_object_or_404(CustomUser,id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST , instance=user)
        if form.is_valid():     
            form.save()
            # Redirect based on the role of the logged-in user
            return redirect('view_self_record')  
            # if request.user.role == 'admin' or request.user.is_superuser:
            #     return redirect('manage_company_records')
            # elif request.user.role == 'ceo':
            #     return redirect('manage_company_records')
            # elif request.user.role == 'team_lead':
            #     return redirect('manage_team_records')
            # elif request.user.role == 'employee':
            #     return redirect('view_self_record')
        
                
    else:
        form =CustomUserChangeForm(instance=user)
    return render(request,'edit_user.html',{'form':form})  

def delete_user(request,user_id):
    user=get_object_or_404(CustomUser,id=user_id)
    if request.method== 'POST':
        user.delete()
        print(user.role)
        # Redirect based on the role of the logged-in user
        if request.user.role == 'admin' or request.user.is_superuser:
            return redirect('manage_company_records')
        elif request.user.role == 'ceo':
            return redirect('manage_company_records')
        elif request.user.role == 'team_lead':
            return redirect('manage_team_records')
        elif request.user.role == 'employee':
            return redirect('view_self_record')
    return render (request,'confirm_delete.html' , {'user':user})

def search_users(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    users = CustomUser.objects.filter(company=request.user.company)

    if query:
        users = users.filter(username__icontains=query) | users.filter(role__icontains=query )

    return render(request, 'company_records.html', {'records': users, 'query': query})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login') 
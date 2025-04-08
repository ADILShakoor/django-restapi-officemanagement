from django.shortcuts import render
from .models import Project,Task
from django.shortcuts import redirect
from .forms import ProjectForm,AssignEmployeeForm , TaskForm,TaskRemarkform
from django.shortcuts import get_object_or_404
from my_app.models import CustomUser



# Create your views here.

def list_projects(request):
    if request.user.role not in ['ceo', 'team_lead']:
        return render(request, '403.html')  # Forbidden

    projects = Project.objects.filter(company=request.user.company)
    return render(request, 'project_management/list_projects.html', {'projects': projects})

def add_project(request):
    if request.user.role not in ['ceo', 'team_lead']:
        return render(request, '403.html')  # Forbidden

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.company = request.user.company
            project.created_by = request.user
            project.save()
            form.save_m2m()  # Save ManyToMany relationships 
            return redirect('list_projects') 
    else:
        form = ProjectForm()

    return render(request, 'project_management/add_project.html', {'form': form})


def assign_employees(request, project_id):
    # project=get_object_or_404(Project, id=project_id)
    if request.user.role not in ['ceo', 'team_lead'] :
        return render(request, '403.html')  # Forbidden

    project = get_object_or_404(Project, id=project_id, company=request.user.company)

    if request.method == 'POST': 
        form = AssignEmployeeForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            project.assigned_employees.add(employee)
            # form.save()
            # return redirect('list_projects')
            return redirect('assign_employees', project_id=project.id)
    else:
        form = AssignEmployeeForm()
        # Update form queryset to exclude already assigned employees
        form.fields['employee'].queryset = CustomUser.objects.filter(
            role='employee', 
            assigned_projects=None, 
            company=project.company  # Ensuring employees are from the same company
        )
    return render(request, 'project_management/assign_employees.html', {'form': form, 'project': project})


def assign_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Ensure only the related Team Lead can assign tasks
    if request.user.role != 'team_lead' or request.user.company != project.company:
        return render(request, '403.html')  # Forbidden

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('list_projects')
            
    else:
        form = TaskForm(project=project)

    return render(request, 'project_management/assign_task.html', {'form': form, 'project': project})

def projects_detail(request,project_id):
    # Get all projects created by the logged-in user
    # user_projects = Project.objects.filter(created_by=request.user)
    project = get_object_or_404(Project, id=project_id)
    user_tasks = Task.objects.filter(project=project)
    # Get all tasks related to those projects
    # user_tasks = Task.objects.filter(project__in=user_projects)
    return render(request, 'project_management/project_detail.html', {'user_tasks': user_tasks})

def task_remarks(request,task_id): 
    task=get_object_or_404(Task,id=task_id)
    if request.method=='POST':
        form=TaskRemarkform(request.POST, instance=task)
        if form.is_valid():
            # form.save(commit=False)     only use when we change values or edited values by view
            # task_form.assigned_to=request.user
            form.save()
            if request.user.role == 'team_lead':
               return redirect('projects-detail', project_id=task.project.id)
            else:
                return redirect('view_self_taskes')
    else:
        form=TaskRemarkform(instance=task)
    return render(request,'project_management/task_remark.html',{"form":form})   
    
    

from django.shortcuts import render, get_object_or_404, redirect
from .models import Job, JobApplication
from .forms import JobApplicationForm
from .forms import JobForm


def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobMang/job_list.html', {'jobs': jobs})

def apply_for_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()
            return render(request, 'jobMang/application_success.html', {'job': job})
    else: 
        form = JobApplicationForm()

    return render(request, 'jobMang/job_application_form.html', {'form': form, 'job': job})


def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job-list')
    else:
        form = JobForm()
    return render(request, 'jobMang/job_create_form.html', {'form': form})

def applicant_list(request):
    
    applications = JobApplication.objects.all()
    return render(request, 'jobMang/applicant_list.html', {'applications': applications})


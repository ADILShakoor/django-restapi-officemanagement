from django.urls import path
from . import views

# root url= jobMang/

urlpatterns = [
    path('', views.job_list, name='job-list'),
    path('create/', views.create_job, name='create-job'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply-for-job'),
    path('applicants/', views.applicant_list, name='applicant-list'),
  
]

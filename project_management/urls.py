from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# root URL = project/
urlpatterns = [
    path('', views.list_projects, name='list_projects'),
    path('add/', views.add_project, name='add_project'),
    path('<int:project_id>/assign/', views.assign_employees, name='assign_employees'),
    #  path('assign-employee/<int:project_id>/', assign_employee, name='assign_employee'),
    path('<int:project_id>/assign_task/',views.assign_task,name='assign_task'),
    path('<int:project_id>/projects_detail/', views.projects_detail, name='projects-detail'),
    path('task_remarks/<int:task_id>/', views.task_remarks, name='task-remarks'),

]
# Serve media files during development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views

# root url ---->  projectAPI

urlpatterns = [
    # path("projectapi/",views.ProjectApiView.as_view()),
    # path("taskapi/",views.TaskApiView.as_view()),
    path("projects/",views.Projectapi.as_view()),
    path("tasks/",views.TaskApi.as_view()),
    path("projects/<int:project_id>",views.ProjectDetailAPIView.as_view()),
    path("tasks/<int:task_id>",views.TaskDetailAPIView.as_view())
]
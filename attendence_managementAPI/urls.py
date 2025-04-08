from django.urls import path
from . import views
# rooturl ---> attendenceAPI

urlpatterns = [
    path('attendances/', views.attendance_list_create, name='attendance-list-create'),
    path('attendances/<int:pk>/', views.attendance_detail, name='attendance-detail'),

    path('leave-applications/', views.leave_application_list_create, name='leave-application-list-create'),
    path('leave-applications/<int:pk>/', views.leave_application_detail, name='leave-application-detail'),

    path('leave-types/', views.leave_type_list_create, name='leave-type-list-create'),
    path('leave-types/<int:pk>/', views.leave_type_detail, name='leave-type-detail'),
]

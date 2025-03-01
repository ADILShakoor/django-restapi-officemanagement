from django.urls import path
from .import views
# root url attendence
urlpatterns = [
    
    path("attendance_create/",views.attendance_create,name='attendance-create'),
    path('attendance_list/', views.attendance_list, name='attendance-list'),
    path('attendance_update/<int:pk>', views.attendance_update, name='attendance-update'),
    path("attendance_delete/<int:id>",views.attendance_delete  ,name="attendance-delete"),
    path('leave-applications/', views.leave_list, name='leave-application-list'),
    path("add_leave_categorey/",views.add_leave_categorey,name="add-leave-categorey"),
    path('leave-applications/create/', views.leave_create, name='leave-application-create'),   
    path('leave-applications/<int:pk>/approval/', views.leave_approval, name='leave-applications-aprovel'),  
    path('leave-applications/<int:pk>/update/', views.leave_update, name='leave-application-update'), 
    path('leave-applications/<int:pk>/delete/', views.leave_delete, name='leave-application-delete'),  
]
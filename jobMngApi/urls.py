from . import  views
from django.urls import path

urlpatterns = [
    path('postjob/', views.postjob, name='postjob'),
    path('getjob/', views.getjob, name='getjob'),
    # path('applyjob/', views.applyjob, name='applyjob'),
    # path('getapplication/', views.getapplication, name='getapplication'),
    # path('updateapplication/<int:pk>/', views.updateapplication, name='updateapplication'),
    # path('deleteapplication/<int:pk>/', views.deleteapplication, name='deleteapplication'),
]
from django.urls import path
from . import views
# root url for app = document-mng
urlpatterns = [
    path('documents/', views.document_list, name='document-list'),
    path('documents/upload/', views.document_upload, name='document-upload'),
    path('documents/<int:pk>/', views.document_detail, name='document-detail'),
]

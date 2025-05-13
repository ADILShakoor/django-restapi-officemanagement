from django.urls import path
from . import views
# rootUrl---> document-mngAPI/
urlpatterns = [
    path('documents/', views.document_listAPI, name='document-listAPI'),
    path('documents/upload', views.upload_document, name='document-upload'),
    path('documents/<int:pk>/', views.employee_document_detail, name='document-detail'),
]

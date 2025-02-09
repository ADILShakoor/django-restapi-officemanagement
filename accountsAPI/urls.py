from django.urls import path
from .views import UserListAPIView

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='user-list'),
]

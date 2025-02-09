from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from my_app.models import CustomUser
from .serializers import CustomUserSerializer

class UserListAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

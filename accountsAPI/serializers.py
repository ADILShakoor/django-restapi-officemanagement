from rest_framework import serializers
from my_app.models import CustomUser  # Import your model

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'company']

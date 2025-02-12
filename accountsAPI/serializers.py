from rest_framework import serializers
from my_app.models import CustomUser  # Import your model
from rest_framework.decorators import api_view
from my_app.models import Company
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=Company
        fields=["id",'name','created_at']


class CustomUserSerializer(serializers.ModelSerializer):
    
    company=CompanySerializer(read_only=True)
    company_name=serializers.CharField(write_only=True)
    password=serializers.CharField(write_only=True,required=False)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role', 'company',"company_name"]
        # depth=1
        # data validation 
    def create(self,validated_data):
        company_name=validated_data.pop('company_name',None) #get company name from request
        password=validated_data.pop("password")
        validated_data["password"]=make_password(password)
        user=CustomUser.objects.create(**validated_data) # create user instance
        
        if company_name:
            company,_ =Company.objects.get_or_create(name=company_name) # fetch or create  company
            user.company=company    #assing company to user
        user.save()
        return user
    
    def update(self, instance, validated_data):
        company_name = validated_data.pop('company_name', None)

        # Only update password if provided
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)  # Hash the new password

        # Update company if a new one is provided
        if company_name:
            company, _ = Company.objects.get_or_create(name=company_name)
            instance.company = company

        # Update other fields
        return super().update(instance, validated_data)
        
    
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)

    def validate(self, data):
        user=authenticate(username=data['username'],password=data['password'])
        if not user:
            raise serializers.ValidationError({'message':"please enter valid username or password"})
        token,created=  Token.objects.get_or_create(user=user) 
        return  {"token":token.key,"user-id":user.id,"username":user.username,"role":user.role}
        
        # return super().validate(data)
    
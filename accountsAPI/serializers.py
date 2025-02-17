from rest_framework import serializers
from my_app.models import CustomUser  
from rest_framework.decorators import api_view
from my_app.models import Company
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.cache import cache
# abbcj


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
        company_name=validated_data.pop('company_name',None)
        password=validated_data.pop("password")
        validated_data["password"]=make_password(password)
        user=CustomUser.objects.create(**validated_data) # create user instance
        
        if company_name:
            company,_ =Company.objects.get_or_create(name=company_name) 
            user.company=company    
        user.save()
        # Clear cached user list
        cache.delete_pattern("user_list_*")  
        return user
    
    def update(self, instance, validated_data):
        company_name = validated_data.pop('company_name', None)
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)  # Hash the new password     
        if company_name:
            company, _ = Company.objects.get_or_create(name=company_name)
            instance.company = company
        # Update other fields
        updated_instance= super().update(instance, validated_data)
        # cache implementation
        # Clear cached user list
        cache.delete_pattern("user_list_*")  

        return updated_instance
        
    
# class LoginSerializer(serializers.Serializer):
#     username=serializers.CharField()
#     password=serializers.CharField(write_only=True)

#     def validate(self, data):
#         user=authenticate(username=data['username'],password=data['password'])
#         if not user:
#             raise serializers.ValidationError({'message':"please enter valid username or password"})
#         token,created=  Token.objects.get_or_create(user=user) 
#         return  {"token":token.key,"user-id":user.id,"username":user.username,"role":user.role}
        
        # return super().validate(data)
    
    #  update code for login serializer to store token key and send with each request

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    confirm_password=serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] !=data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match!"})
        # return data
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError({'message': "Invalid username or password"})

        token, created = Token.objects.get_or_create(user=user)

        # Set token in cookies
        self.context['response'].set_cookie(
            key="auth_token",
            value=token.key,
            httponly=True,  # Prevent JavaScript access
            secure=True,    # Ensure HTTPS is used
            samesite="Lax"  # Helps prevent CSRF attacks
        )

        return {
            "token": token.key,
            "user_id": user.id,
            "username": user.username,
            "role": user.role
        }

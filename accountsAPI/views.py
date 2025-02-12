from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics,permissions
from rest_framework.views import APIView

# Create your views here.
from my_app.models import CustomUser
from .serializers import CustomUserSerializer,LoginSerializer
from .permissions import CustomUserPermission


# api_view(['GET','POST'])
# def users_view(request):
#     pass
class RegisterUser(generics.CreateAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=CustomUserSerializer
    

class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            return Response(serializer.validated_data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    
    
class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.select_related("company").all()
    serializer_class = CustomUserSerializer
    permission_classes=[CustomUserPermission] #permissions.IsAuthenticated,
    
    def get_queryset(self):
        user = self.request.user

        # Super Admin: Get all users
        if user.is_superuser:
            return CustomUser.objects.select_related("company").all()

        # Admin: Get all users in the same company
        elif user.role == 'admin' or user.role=="ceo":
            return CustomUser.objects.filter(company=user.company)

        # Team Lead: Get all employees in the same company
        elif user.role == 'team_lead':
            return CustomUser.objects.filter(company=user.company, role='employee')

        # Employee: Can only see their own record
        elif user.role == 'employee':
            return CustomUser.objects.filter(id=user.id)

        return CustomUser.objects.none()  # Return empty queryset if no permission

# api_view(["GET","POST","PUT","PATCH","DELETE"])
# def company_data(request):
#     users=CustomUser.objects.all()
#     if request.method=='GET':


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API for viewing, updating, and deleting users based on role-based permissions.
    - Super Admin: Can update and delete any user.
    - Admin: Can update and delete users in their company.
    - Team Lead: Can update employees in their company but cannot delete them.
    - Employee: Can only update their own record and cannot delete.
    """
    serializer_class = CustomUserSerializer
    permission_classes = [CustomUserPermission]  #permissions.IsAuthenticated,

    def get_queryset(self):
        user = self.request.user
        
        # Super Admin: Access to all users
        if user.is_superuser:
            return CustomUser.objects.select_related("company").all()

        # Admin: Access users in the same company
        elif user.role == 'admin' or user.role=="ceo":
            return CustomUser.objects.filter(company=user.company)

        # Team Lead: Access employees in the same company
        elif user.role == 'team_lead':
            return CustomUser.objects.filter(company=user.company, role='employee')

        # Employee: Can only access their own record       user.role == 'employee'
        else:
            return CustomUser.objects.filter(id=user.id)

        # return CustomUser.objects.none()  # Deny access otherwise
        # return user 
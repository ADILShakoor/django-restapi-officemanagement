from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics,permissions
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
from django.core.paginator import Paginator,EmptyPage
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter 
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
# Create your views here.
from my_app.models import CustomUser
from .serializers import CustomUserSerializer,LoginSerializer
from .permissions import CustomUserPermission

#implement all the buildin terms ---> pagination,throttling,authentication , authurization ,permisssions,generic classes , API view Class,filtering,seraching,oredering and CRUD operations



class RegisterUser(generics.CreateAPIView):
    throttle_classes=[AnonRateThrottle] 
    queryset=CustomUser.objects.all()
    serializer_class=CustomUserSerializer
      

# class LoginView(APIView):
#     def post(self,request):
#         serializer=LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             # serializer.save()
#             return Response(serializer.validated_data,status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    # update code for login  store and retrives token in cookies 


class LoginView(APIView):
    def post(self, request):
        response = Response()
        serializer = LoginSerializer(data=request.data, context={'response': response})

        if serializer.is_valid():
            response.data = serializer.validated_data  # Send token in response body
            response.status_code = status.HTTP_200_OK
            return response  # Return response with token in cookies

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserObjPagination(PageNumberPagination):
    page_size=5                   
    page_size_query_params="page_size"   
    max_page_size=10
    
class UserListAPIView(generics.ListAPIView):
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    pagination_class= UserObjPagination 
    # queryset = CustomUser.objects.select_related("company").all()
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields=['username','role']
    filterset_fields=['company','role'] 
    ordering_fields= ["username"]
    serializer_class = CustomUserSerializer
    permission_classes=[IsAuthenticated] #permissions.IsAuthenticated,
    
    #Cache the entire view for 10 minutes
    @method_decorator(cache_page(60 * 10))  
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
    def get_queryset(self):
        user = self.request.user
        cache_key = f"user_list_{user.role}_{user.company_id}"  # Unique cache key
         # Check if cached data exists
        cached_queryset = cache.get(cache_key)
        if cached_queryset:
            return cached_queryset  # Return cached data

        if user.is_superuser:
            # return CustomUser.objects.select_related("company").all()
            queryset=CustomUser.objects.select_related("company").all()
        elif user.role == 'admin' or user.role=="ceo":
            queryset= CustomUser.objects.filter(company=user.company)
        elif user.role == 'team_lead':
            queryset= CustomUser.objects.filter(company=user.company, role='employee')
        elif user.role == 'employee':
            queryset= CustomUser.objects.filter(id=user.id)

        else:
            queryset=CustomUser.objects.none() 
        cache.set(cache_key, queryset, timeout=60 * 10)  # ✅ Cache for 10 minutes
        return queryset

# api_view(["GET","POST","PUT","PATCH","DELETE"])
# def company_data(request):
#     users=CustomUser.objects.all()
#     if request.method=='GET':


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = CustomUser.objects.select_related("company").all()
    serializer_class = CustomUserSerializer
    # permission_classes = [IsAuthenticated,CustomUserPermission] 
    def get_throttles(self):
        if self.request.method == 'GET':
           throttle_classes = [AnonRateThrottle,UserRateThrottle]     #UserRateThrottle
        else:
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser:
            return CustomUser.objects.select_related("company").all()
        
        elif user.role == 'admin' or user.role=="ceo":
            return CustomUser.objects.filter(company=user.company)
        elif user.role == 'team_lead':
            return CustomUser.objects.filter(company=user.company, role='employee')
        else:
            return CustomUser.objects.filter(id=user.id)

        # return CustomUser.objects.none()  # Deny access otherwise
        # return user 
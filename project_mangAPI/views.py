from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
# Create your views here.
from project_management.models import Task,Project
from .serializer import ProjectSerializer,TaskSerializer

class ProjectsPagination(PageNumberPagination):
    page_size=3
    page_query_param=("page_size")
    max_page_size=5

  
class Projectapi(APIView):
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    permission_classes=[IsAuthenticated]
    # filter_backends=[DjangoFilterBackend]
    # filter_set_fields=["name"]
    # pagination_class=ProjectsPagination
    # def get(self,request):
    #     projects=Project.objects.all()
    #     pagintor=ProjectsPaginationdjna
    #     serializer=ProjectSerializer(projects,many=True)
    #     return Response(serializer.data)

    def get(self, request):
        user=self.request.user
        if user.role=="admin" or user.role=="ceo" or user.role=="team_lead":
           projects = Project.objects.filter(company=user.company)
           paginator = ProjectsPagination()
           search=self.request.query_params.get("search")
           if search:
               projects=projects.filter(name__icontains=search)
            
           paginated_projects = paginator.paginate_queryset(projects, request)
           return paginator.get_paginated_response(ProjectSerializer(paginated_projects, many=True).data)
        else:
            return Response({"message":"you are not Allow to get that"})

    def post(self,request):
        
        serializer=ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    
class TaskApi(APIView):
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    permission_classes=[IsAuthenticated]
    # def get(self,request):
    #     tasks=Task.objects.all()
    #     serializer=TaskSerializer(tasks,many=True)
    #     return Response(serializer.data)
    def get(self,request):
           user=self.request.user
        #    tasks=Task.objects.filter(company=user.company) 
           tasks=Task.objects.all()
           paginator=ProjectsPagination()
           paginated_tasks=paginator.paginate_queryset(tasks,request)
           return paginator.get_paginated_response(TaskSerializer(paginated_tasks,many=True).data)
     
           
    def post(self,request):
        serializer=TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


class ProjectDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, project_id):
        return get_object_or_404(Project, id=project_id)
    
    def get(self,request,project_id):
        projects=self.get_object(project_id)
        serializer=ProjectSerializer(projects)
        return Response(serializer.data)
    
    def put(self, request, project_id): 
        project = self.get_object(project_id)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, project_id):  
        project = self.get_object(project_id)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id):  
        project = self.get_object(project_id)
        project.delete()
        return Response({"message": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, task_id):
        return get_object_or_404(Task, id=task_id)
    
    def get(self,request,task_id):
        tasks=self.get_object(task_id)
        serializer=TaskSerializer(tasks)
        return Response(serializer.data)
    
    def put(self, request, task_id): 
        task = self.get_object(task_id)
        serializer = TaskSerializer(task, data=request.data)
        # file handling
        if 'image' in request.FILES:
            request.data['image'] = request.FILES['image']
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, task_id):
        task = self.get_object(task_id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if 'image' in request.FILES:
            request.data['image'] = request.FILES['image']
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        task = self.get_object(task_id)
        task.delete()
        return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

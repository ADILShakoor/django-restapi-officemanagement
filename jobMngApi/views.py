from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes, throttle_classes
from .serializers import EmployeeDocumentSerializer,JobAdSerializer
from jobMng.models import JobApplication
from jobMng.models import Job

def postjob(request):
    if request.method == 'POST':
        serializer = JobAdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    return render(request, 'postjob.html')
def getjob(request):
    if request.method == 'GET':
        jobs=Job.objects.all()
        serializer = JobAdSerializer(jobs, many=True)
        return Response(serializer.data, status=200)
def applyjob(request): 
    if request.method == 'POST':
        serializer = EmployeeDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    return render(request, 'applyjob.html')
def jobapplications(request):
    if request.method == 'GET':
        applications = JobApplication.objects.all()
        serializer = EmployeeDocumentSerializer(applications, many=True)
        return Response(serializer.data, status=200)
    return render(request, 'jobapplications.html')
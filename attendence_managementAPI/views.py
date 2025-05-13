from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from attendence_management.models import Attendance, LeaveApplication, LeaveType
from .serializers import AttendanceSerializer, LeaveApplicationSerializer, LeaveTypeSerializer

# Attendance List and Create
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def attendance_list_create(request):
    if request.method == "GET":
        attendances = Attendance.objects.filter(company=request.user.company)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Attendance Retrieve, Update, Delete
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def attendance_detail(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk, company=request.user.company)

    if request.method == "GET":
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        serializer = AttendanceSerializer(attendance, data=request.data, partial=(request.method == "PATCH"))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        attendance.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# Leave Applications List and Create
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def leave_application_list_create(request):
    if request.method == "GET":
        leaves = LeaveApplication.objects.filter(company=request.user.company)
        serializer = LeaveApplicationSerializer(leaves, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = LeaveApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=request.user, company=request.user.company, status="pending")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Leave Application Retrieve, Update, Delete
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def leave_application_detail(request, pk):
    leave = get_object_or_404(LeaveApplication, pk=pk, company=request.user.company)

    if request.method == "GET":
        serializer = LeaveApplicationSerializer(leave)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        serializer = LeaveApplicationSerializer(leave, data=request.data, partial=(request.method == "PATCH"))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        leave.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def leave_type_list_create(request):
    if request.method == "GET":
        leave_types = LeaveType.objects.all()
        serializer = LeaveTypeSerializer(leave_types, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = LeaveTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Leave Type Retrieve, Update, Delete
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def leave_type_detail(request, pk):
    leave_type = get_object_or_404(LeaveType, pk=pk)

    if request.method == "GET":
        serializer = LeaveTypeSerializer(leave_type)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        serializer = LeaveTypeSerializer(leave_type, data=request.data, partial=(request.method == "PATCH"))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        leave_type.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

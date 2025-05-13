from django.shortcuts import render , get_object_or_404
from rest_framework.decorators import api_view, permission_classes, parser_classes,throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from document_management.models import EmployeeDocument
from .serializers import EmployeeDocumentSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle

class CoustomPagination(PageNumberPagination):
    page_size=3
    page_query_param=("page_size")
    max_page_size=5
    
class CoustomUserThrottling(UserRateThrottle):
    rate='5/min'
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@throttle_classes([CoustomUserThrottling])
def document_listAPI(request):
    if request.user.role == 'hr' or request.user.is_superuser:
        documents = EmployeeDocument.objects.all()
    else:
        documents = EmployeeDocument.objects.filter(employee=request.user)
    
    search_query=request.GET.get('search')
    filter_query=request.GET.get('is-signed')
    ordering=request.GET.get('ordering')
    if ordering:
        documents=documents.order_by(ordering)
    if filter_query:
        documents=documents.filter(is_signed=filter_query)
    if search_query:
        documents= documents.filter(document_type__icontains=search_query)
    paginator=CoustomPagination()
    pagination_qz=paginator.paginate_queryset(documents, request)
    
    serializer = EmployeeDocumentSerializer(pagination_qz, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_document(request): 
    # data = request.data.copy()
    # if request.user.role != 'hr':  
    #     data['employee'] = request.user.id

    serializer = EmployeeDocumentSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_document(request, pk):
#     try:
#         document = EmployeeDocument.objects.get(pk=pk)

#         if request.user.role != 'hr' and document.employee != request.user:
#             return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

#         serializer = EmployeeDocumentSerializer(document)
#         return Response(serializer.data)
#     except EmployeeDocument.DoesNotExist:
#         return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])  # Required for file upload
def employee_document_detail(request, pk):
    role=request.user.role
    print(role)
    document = get_object_or_404(EmployeeDocument, pk=pk)

    if role=='hr' and request.method == 'GET':
        serializer = EmployeeDocumentSerializer(document, context={'request': request})
        return Response(serializer.data)

    elif role=="hr" and request.method == 'PUT':
        serializer = EmployeeDocumentSerializer(document, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.update(document, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif role=="hr" and request.method == 'PATCH':
        serializer = EmployeeDocumentSerializer(document, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.update(document, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        document.delete()
        return Response({'message': 'Document deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"message":"you have no permission to see data"})

from django.shortcuts import render
from rest_framework import generics,viewsets,status
from rest_framework.response import Response
from django.shortcuts import  get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator,EmptyPage
from accountsAPI.permissions import CustomUserPermission
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
from .throttling import AssetRateThrolling
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from my_asset.models import Asset
from .serializer import AssetSerializer
from accountsAPI.permissions import CustomUserPermission
 

class AssertViewGeneric(generics.ListCreateAPIView):
    queryset=Asset.objects.all()
    serializer_class= AssetSerializer
    
class singleAssetView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Asset.objects.all()
    serializer_class=AssetSerializer

# pagination 
# class AssetItemsPaginator(PageNumberPagination):
#     page_size=3
#     page_size_query_param="page-size"
#     max_page_size=10
# class AssetRateThrolling(SimpleRateThrottle):
#     cope = 'burst'
#     rate = '6/minute' 
class AssertView(viewsets.ViewSet):
    permission_classes=[IsAuthenticated,CustomUserPermission]
    # pagination_class=AssetItemsPaginator
    # throttle_classes=[AssetRateThrolling]
    
    def list(self,request): 
        # get request for list of assets
        user=self.request.user
        self.throttle_classes=[AnonRateThrottle,UserRateThrottle]
        assets=Asset.objects.filter(company=user.company)
        perpage=self.request.query_params.get("perpage",default=3)
        page=self.request.query_params.get("page",default=1)
        search=self.request.query_params.get("search")
        user_name=self.request.query_params.get("assigned_to") 
        by_company=self.request.query_params.get("company")
        ordering=self.request.query_params.get("ordering")
        if ordering:
            assets=assets.order_by(ordering)
        if by_company:
            assets=assets.filter(company__name=by_company)
        if user_name:
            assets=assets.filter(assigned_to__username=user_name)
        if search:
            assets=assets.filter(name__icontains=search)
            
        paginator=Paginator(assets,per_page=perpage) 
        try:
          assets=paginator.page(number=page)
        except EmptyPage:
          assets=[]
        serializer=AssetSerializer(assets,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk=None):
        # retrieve single asset if id exits  
        asset=get_object_or_404(Asset,id=pk)
        serializer= AssetSerializer(asset,many=False)
        return Response(serializer.data)
    
    def create(self,request):
        #make POST call to create new resource 
        serializer=AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,pk=None):
        try:
            asset=Asset.objects.get(id=pk)
        except Asset.DoesNotExist:
            return Response({"message":"book Not Found with that id"})
        serializer=AssetSerializer(asset,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self,request,pk=None):
        asset=get_object_or_404(Asset,id=pk)
        serializer=AssetSerializer(asset,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk=None):
        asset=get_object_or_404(Asset,id=pk)
        if asset:
            asset.delete()
            return Response({"message":"delete sccessfully"},status=status.HTTP_204_NO_CONTENT)
            

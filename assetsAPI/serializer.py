from my_asset.models import Asset, AssertCategory
from rest_framework import serializers
from my_app.models import CustomUser,Company
# from accountsAPI.serializers import CompanySerializer

class  AssertCategorySerializer(serializers.ModelSerializer):  
    class Meta:
        model=AssertCategory
        fields="__all__"
class companySerilizer(serializers.ModelSerializer):
    class Meta:
        model=Company
        fields='__all__'
        
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields='__all__' 

class AssetSerializer(serializers.ModelSerializer):
    category=AssertCategorySerializer(read_only=True)
    category_id=serializers.IntegerField(write_only=True)
    company=companySerilizer(read_only=True) 
    company_id=serializers.IntegerField(write_only=True)
    assigned_to=CustomUserSerializer(read_only=True)
    assigned_to_id=serializers.IntegerField(write_only=True)
    class Meta:
      model=Asset
      fields=['id','name',"category","company","serial_number",'purchase_date',"value","status","assigned_to","maintenance_date","description",'category_id',"company_id","assigned_to_id"]
      
    # def create(self,validated_data):
        

 

# from rest_framework import serializers
# from .models import AssertCategory, Asset

# class AssertCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AssertCategory
#         fields = '__all__'
        
# class CustomUserserializer(serializers.ModelSerializer):
#     class Meta:
#         model=CustomUser
#         fields = '__all__'

# class AssetSerializer(serializers.ModelSerializer):
#     category = AssertCategorySerializer(read_only=True)
#     category_id = serializers.PrimaryKeyRelatedField(
#         queryset=AssertCategory.objects.all(), write_only=True, source='category'
#     )

#     class Meta:
#         model = Asset
#         fields = '__all__'


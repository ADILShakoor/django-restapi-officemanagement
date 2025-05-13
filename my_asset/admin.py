from django.contrib import admin
from .models import Asset,AssertCategory,AssetAssignmentHistory
# Register your models here.


admin.site.register(AssertCategory)
admin.site.register(Asset)
admin.site.register(AssetAssignmentHistory)

# @admin.register(AssertCategory)
# class AssertCategoryAdmin(admin.ModelAdmin):
#     list_display =['name','decription']  
    
# @admin.register(Asset)
# class AssetAdmin(admin.ModelAdmin):
#     list_display = ['name', 'category', 'status', 'assigned_to', 'company', 'purchase_date']
#     list_filter = ['status', 'category', 'company']
#     search_fields = ['name', 'serial_number']

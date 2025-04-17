from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import EmployeeDocument

@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'document_type', 'title', 'uploaded_on', 'expires_on', 'is_signed')
    search_fields = ('employee__username', 'title')
    list_filter = ('document_type', 'is_signed', 'expires_on')

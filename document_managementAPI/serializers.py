from rest_framework import serializers
from document_management.models import EmployeeDocument
from rest_framework import serializers
from datetime import date
from document_management.models import EmployeeDocument
from django.contrib.auth import get_user_model
from my_app.models import CustomUser


# class EmployeeDocumentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EmployeeDocument  
#         fields = ['id', 'employee', 'document_type', 'file', 'uploaded_on', 'expires_on', 'notes']
#         read_only_fields = ['id', 'uploaded_at']



# User = CustomUser

class EmployeeDocumentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    employee = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.none())
    company = serializers.CharField(required=False, allow_blank=True)
    document_type = serializers.ChoiceField(choices=[choice for choice in EmployeeDocument._meta.get_field('document_type').choices])
    title = serializers.CharField(max_length=255)
    file = serializers.FileField(allow_null=True, required=False)
    uploaded_on = serializers.DateTimeField(read_only=True)
    expires_on = serializers.DateField(required=False, allow_null=True)
    is_signed = serializers.BooleanField(default=False)
    signature_link = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    notes = serializers.CharField(allow_blank=True, required=False)
    is_expired = serializers.SerializerMethodField()
    days_until_expiry = serializers.SerializerMethodField()
    def __init__(self, *args, **kwargs):
        super(EmployeeDocumentSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and hasattr(request.user, 'company'):
            self.fields['employee'].queryset = CustomUser.objects.filter(company=request.user.company)

    def create(self, validated_data):
        return EmployeeDocument.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def get_is_expired(self, obj):
        return obj.is_expired()

    def get_days_until_expiry(self, obj):
        return obj.days_until_expiry()

    def create(self, validated_data):
        return EmployeeDocument.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

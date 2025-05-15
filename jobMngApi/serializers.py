from rest_framework import serializers
from jobMng.models import Job, JobApplication
from rest_framework import serializers
from datetime import date
from django.contrib.auth import get_user_model
from my_app.models import CustomUser


class JobAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["description","location","last_date_to_apply","posted_on"]
        read_only_fields = ["id"]



# User = CustomUser

class EmployeeDocumentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.none())
    name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=255)
    address = serializers.FileField(allow_null=True, required=False)
    experience_years = serializers.IntegerField(required=False)
    company = serializers.CharField(required=False, allow_null=True)
    cover_letter = serializers.CharField(default=False)
    resume = serializers.FileField(required=True)
    applied_on = serializers.CharField(allow_blank=True, required=False)
    
    # def __init__(self, *args, **kwargs):
    #     super(EmployeeDocumentSerializer, self).__init__(*args, **kwargs)
    #     request = self.context.get('request', None)
    #     if request and hasattr(request.user, 'company'):
    #         self.fields['employee'].queryset = CustomUser.objects.filter(company=request.user.company)

    # def create(self, validated_data):
    #     return EmployeeDocument.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance

    # def get_is_expired(self, obj):
    #     return obj.is_expired()

    # def get_days_until_expiry(self, obj):
    #     return obj.days_until_expiry()

    # def create(self, validated_data):
    #     return EmployeeDocument.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance

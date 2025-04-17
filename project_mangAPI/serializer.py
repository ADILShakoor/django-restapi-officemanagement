from rest_framework import serializers
from project_management.models import Project,Task
from my_app.models import Company,CustomUser


# class projectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Project
#         fields="__all__"
        
# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Task
#         fields="__all__"
# coustom serializer 
class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    status = serializers.ChoiceField(choices=Project.STATUS_CHOICES, default='ongoing')
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    assigned_employees = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True, required=False)
    start_date = serializers.DateField()
    end_date = serializers.DateField(required=False, allow_null=True)

    def validate(self, data):
        
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if end_date and start_date > end_date:
            raise serializers.ValidationError("End date cannot be before start date.")
        return data

    def validate_assigned_employees(self, employees):
    
        company = self.initial_data.get('company')
        if company:
            company_instance = Company.objects.get(id=company)
            for employee in employees:
                if employee.company != company_instance:
                    raise serializers.ValidationError(f"{employee.username} does not belong to this company.")
        return employees

    def create(self, validated_data):
        
        assigned_employees = validated_data.pop('assigned_employees', [])
        project = Project.objects.create(**validated_data)
        project.assigned_employees.set(assigned_employees)
        return project

    def update(self, instance, validated_data):
       
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)

        if 'assigned_employees' in validated_data:
            instance.assigned_employees.set(validated_data['assigned_employees'])

        instance.save()
        return instance

 
class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(role='employee'), allow_null=True, required=False)
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES, default='pending')
    weight = serializers.IntegerField(default=1)
    due_date = serializers.DateField()
    image = serializers.ImageField(allow_null=True, required=False)

    def validate_assigned_to(self, employee):
        
        project = self.initial_data.get('project')
        if project and employee:
            project_instance = Project.objects.get(id=project)
            if employee.company != project_instance.company:
                raise serializers.ValidationError(f"{employee.username} does not belong to the project's company.")
        return employee

    def validate_due_date(self, due_date):
        
        from datetime import date
        if due_date < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return due_date

    def create(self, validated_data):
        
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
       
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.project = validated_data.get('project', instance.project)
        instance.assigned_to = validated_data.get('assigned_to', instance.assigned_to)
        instance.status = validated_data.get('status', instance.status)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.image = validated_data.get('image', instance.image)

        instance.save()
        return instance

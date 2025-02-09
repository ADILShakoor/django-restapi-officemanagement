from django.db import models
from my_app.models import CustomUser, Company

class Project(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_projects")
    assigned_employees = models.ManyToManyField(CustomUser, related_name="assigned_projects", blank=True)   #limit_choices_to={'role': 'employee'}
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'employee'})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    weight = models.IntegerField( default=1)  # New weight field
    due_date = models.DateField()
    image = models.ImageField(upload_to='task_images/', blank=True, null=True)  # Task image field

    def __str__(self):
        return f"{self.name} ({self.project.name})"

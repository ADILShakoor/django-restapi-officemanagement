from django.contrib.auth.models import AbstractUser
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
         return self.name


class CustomUser(AbstractUser):
      ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('ceo', 'CEO'),
        ('team_lead', 'Team Lead'),
        ('employee', 'Employee'),
        ('hr','HR'),
    ]
      role = models.CharField(max_length=20, choices=ROLE_CHOICES,default="employee")
      company= models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
      


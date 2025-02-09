from django.db import models
from my_app.models import CustomUser,Company
# Create your models here.

class AssertCategory(models.Model):
    name= models.CharField(max_length=100,unique=True)
    description= models.TextField(blank=True)
    def __str__(self):
        return self.name

    
class Asset(models.Model):
     STATUS_CHOICES = [
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
    ]
     name=models.CharField(max_length=100)
     category= models.ForeignKey(AssertCategory,on_delete=models.CASCADE,related_name='assets')
     company=models.ForeignKey(Company,on_delete=models.CASCADE)
     serial_number=models.CharField(max_length=255,unique=True,blank=True,null=True)
     purchase_date=models.DateField()
     value= models.DecimalField(max_digits=10,decimal_places=2)
     status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="available")
     assigned_to=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,blank=True,null=True,related_name="assigned_assets")
     maintenance_date =models.DateField(blank=True,null=True)
     description=models.TextField(blank=True)
     
     def __str__(self):
         return f' {self.name } {self.company.name} {self.assigned_to.username}'
     
     
    
class AssetAssignmentHistory(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset.name} assigned to {self.assigned_to}"

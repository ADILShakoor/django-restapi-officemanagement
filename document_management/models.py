from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from datetime import date

DOCUMENT_TYPES = [
    ('contract', 'Employment Contract'),
    ('certification', 'Certification'),
    ('license', 'License'),
    ('visa', 'Visa'),
    ('id', 'ID/Passport'),
    ('other', 'Other'),
]

class EmployeeDocument(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    company =models.CharField(max_length=20,null=True,blank=True)
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='employee_documents/')
    uploaded_on = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateField(null=True, blank=True)
    is_signed = models.BooleanField(default=False)
    signature_link = models.URLField(blank=True, null=True, help_text="Link to digital signature service (e.g., DocuSign)")
    notes = models.TextField(blank=True)

    def is_expired(self):
        return self.expires_on and self.expires_on < date.today()

    def days_until_expiry(self):
        if self.expires_on:
            return (self.expires_on - date.today()).days
        return None

    def __str__(self):
        return f"{self.employee.username} - {self.document_type}: {self.title}"

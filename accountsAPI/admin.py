from django.contrib import admin

# Register your models here.
from django.contrib.sessions.models import Session

admin.site.register(Session)  # This allows you to see session data

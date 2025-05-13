from django.db import models
from django.conf import settings
from my_app.models import CustomUser
from project_management.models import Project

EVENT_TYPE_CHOICES = [
    ('meeting', 'Meeting'),
    ('interview', 'Interview'),
    ('task', 'Task'),
]

class CalendarEvent(models.Model):
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='calendar_events'
    )
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='calendar_events',
        null=True,
        blank=True
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    google_event_id = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    google_event_link = models.URLField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.event_type})"

    class Meta:
        ordering = ['-start_time']

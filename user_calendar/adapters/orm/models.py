from django.db import models
import uuid

class UserCalendarModel(models.Model):
    user_id = models.IntegerField(unique=True) # mapping Django User.id 1:1
    calendar_id = models.UUIDField(default=uuid.uuid4, unique=True)

    provider = models.CharField(max_length=50, default="google")

    google_calendar_id = models.CharField(max_length=255, null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

import uuid

from django.db import models


class UserCalendarModel(models.Model):
    user_id = models.IntegerField(unique=True)  # mapping Django User.id 1:1
    calendar_id = models.UUIDField(default=uuid.uuid4, unique=True)

    provider = models.CharField(max_length=50, default="google")

    google_calendar_id = models.CharField(max_length=255, null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

class CategoryModel(models.Model):
    category_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user_id = models.IntegerField()  # maps to Django auth_user.id
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)
    estimated_monthly_cost = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CalendarEventModel(models.Model):
    event_id = models.UUIDField(unique=True)
    user_id = models.IntegerField(db_index=True) # maps to Django auth_user.id

    title = models.CharField(max_length=255)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    estimated_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    category_ids = models.JSONField(default=list)

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
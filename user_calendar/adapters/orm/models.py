import uuid

from django.db import models


class UserCalendarModel(models.Model):
    user_id: models.IntegerField = models.IntegerField(
        unique=True
    )  # mapping Django User.id 1:1
    calendar_id: models.UUIDField = models.UUIDField(default=uuid.uuid4, unique=True)
    provider: models.CharField = models.CharField(max_length=50, default="google")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    google_calendar_id: models.CharField = models.CharField(
        max_length=255, null=True, blank=True
    )
    access_token: models.TextField = models.TextField(null=True, blank=True)
    refresh_token: models.TextField = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "user_calendar"


class CategoryModel(models.Model):
    id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user_id: models.IntegerField = models.IntegerField(db_index=True)

    name: models.CharField = models.CharField(max_length=100)
    color: models.CharField = models.CharField(max_length=20, default="#3b82f6")

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "calendar_category"


class CalendarEventModel(models.Model):
    id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user_id: models.IntegerField = models.IntegerField(
        db_index=True
    )  # maps to Django auth_user.id

    title: models.CharField = models.CharField(max_length=255)
    start_at: models.DateTimeField = models.DateTimeField()
    end_at: models.DateTimeField = models.DateTimeField()

    estimated_cost: models.DecimalField = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    categories: models.ManyToManyField = models.ManyToManyField(
        CategoryModel, related_name="events", blank=True
    )

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "calendar_event"

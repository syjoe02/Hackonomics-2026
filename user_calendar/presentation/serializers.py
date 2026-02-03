from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from rest_framework import serializers

from user_calendar.domain.entities import CalendarEvent, Category, UserCalendar


class UserCalendarSerializer(serializers.Serializer):
    calendar_id = serializers.UUIDField()
    user_id = serializers.IntegerField()
    provider = serializers.CharField()
    created_at = serializers.DateTimeField()

    google_calendar_id = serializers.CharField(allow_null=True)
    access_token = serializers.CharField(allow_null=True)
    refresh_token = serializers.CharField(allow_null=True)

    @classmethod
    def from_domain(cls, calendar: UserCalendar):
        return cls(
            {
                "calendar_id": calendar.calendar_id.value,
                "user_id": calendar.user_id.value,
                "provider": calendar.provider.value,
                "created_at": calendar.created_at.value,

                "google_calendar_id": calendar.google_calendar_id,
                "access_token": calendar.access_token,
                "refresh_token": calendar.refresh_token,
            }
        )

class CategoryCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    color = serializers.CharField()
    estimated_monthly_cost = serializers.DecimalField(max_digits=15, decimal_places=2)

class CategorySerializer(serializers.Serializer):
    category_id = serializers.UUIDField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    color = serializers.CharField()
    estimated_monthly_cost = serializers.DecimalField(max_digits=12, decimal_places=2)
    created_at = serializers.DateTimeField()

    @classmethod
    def from_domain(cls, category: Category):
        return cls({
            "category_id": category.category_id,
            "user_id": category.user_id,
            "name": category.name,
            "color": category.color,
            "estimated_monthly_cost": category.estimated_monthly_cost,
            "created_at": category.created_at.value,
        })
    
class CalendarEventCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    start_at = serializers.DateTimeField()
    end_at = serializers.DateTimeField()
    estimated_cost = serializers.DecimalField(
        max_digits=15, decimal_places=2, required=False, allow_null=True
    )
    category_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        allow_empty=True,
    )


class CalendarEventSerializer(serializers.Serializer):
    event_id = serializers.UUIDField()
    user_id = serializers.IntegerField()
    title = serializers.CharField()
    start_at = serializers.DateTimeField()
    end_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()

    estimated_cost = serializers.DecimalField(
        max_digits=15, decimal_places=2, allow_null=True
    )
    category_ids = serializers.ListField(child=serializers.UUIDField())

    @classmethod
    def from_domain(cls, event: CalendarEvent):
        return cls(
            {
                "event_id": event.event_id.value,
                "user_id": event.user_id.value,
                "title": event.title,
                "start_at": event.start_at,
                "end_at": event.end_at,
                "created_at": event.created_at.value,
                
                "estimated_cost": event.estimated_cost,
                "category_ids": [cid.value for cid in event.category_ids],
            }
        )
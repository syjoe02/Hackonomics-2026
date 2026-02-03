from uuid import UUID
from rest_framework import serializers

from user_calendar.domain.entities import UserCalendar, Category


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

class CategorySerializer(serializers.Serializer):
    category_id = serializers.UUIDField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    color = serializers.CharField()
    estimated_monthly_cost = serializers.DecimalField(max_digits=12, decimal_places=2)

    @classmethod
    def from_domain(cls, category: Category):
        return cls({
            "category_id": category.category_id,
            "user_id": category.user_id,
            "name": category.name,
            "color": category.color,
            "estimated_monthly_cost": category.estimated_monthly_cost,
        })
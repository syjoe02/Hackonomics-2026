from rest_framework import serializers
from uuid import UUID

from user_calendar.domain.entities import UserCalendar
from user_calendar.domain.value_objects import CalendarId, UserId, CalendarProvider, CreatedAt

class ConnectGoogleCalendarSerializer(serializers.Serializer):
    google_calendar_id = serializers.CharField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()

class UserCalendarSerializer(serializers.Serializer):
    calendar_id = serializers.UUIDField()
    user_id = serializers.IntegerField()
    provider = serializers.CharField()
    created_at = serializers.DateTimeField()

    google_calendar_id = serializers.CharField(allow_null=True)
    access_token = serializers.CharField(allow_null=True)
    refresh_token = serializers.CharField(allow_null=True)

    @staticmethod
    def from_domain(calendar: UserCalendar) -> "UserCalendarSerializer":
        return UserCalendarSerializer(
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
from typing import Optional

from django.core.exceptions import ObjectDoesNotExist

from user_calendar.application.ports.repository import UserCalendarRepository
from user_calendar.domain.entities import UserCalendar
from user_calendar.domain.value_objects import (CalendarId, CalendarProvider,
                                                CreatedAt, UserId)

from .models import UserCalendarModel


class DjangoUserCalendarRepository(UserCalendarRepository):

    def save(self, calendar: UserCalendar) -> None:
        UserCalendarModel.objects.update_or_create(
            user_id=calendar.user_id.value,
            defaults={
                "calendar_id": calendar.calendar_id.value,
                "provider": calendar.provider.value,
                "google_calendar_id": calendar.google_calendar_id,
                "access_token": calendar.access_token,
                "refresh_token": calendar.refresh_token,
                "created_at": calendar.created_at.value,
            },
        )

    def find_by_user_id(self, user_id: UserId) -> Optional[UserCalendar]:
        try:
            model = UserCalendarModel.objects.get(user_id=user_id.value)

            return UserCalendar(
                calendar_id=CalendarId(model.calendar_id),
                user_id=UserId(model.user_id),
                provider=CalendarProvider(model.provider),
                created_at=CreatedAt(model.created_at),
                google_calendar_id=model.google_calendar_id,
                access_token=model.access_token,
                refresh_token=model.refresh_token,
            )

        except ObjectDoesNotExist:
            return None

    def find_by_id(self, calendar_id: CalendarId) -> Optional[UserCalendar]:
        try:
            model = UserCalendarModel.objects.get(calendar_id=calendar_id.value)

            return UserCalendar(
                calendar_id=CalendarId(model.calendar_id),
                user_id=UserId(model.user_id),
                provider=CalendarProvider(model.provider),
                created_at=CreatedAt(model.created_at),
                google_calendar_id=model.google_calendar_id,
                access_token=model.access_token,
                refresh_token=model.refresh_token,
            )

        except ObjectDoesNotExist:
            return None

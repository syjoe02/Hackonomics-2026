from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from user_calendar.adapters.orm.models import (
    CalendarEventModel,
    CategoryModel,
    UserCalendarModel,
)
from user_calendar.application.ports.repository import (
    CalendarEventRepository,
    CategoryRepository,
    UserCalendarRepository,
)
from user_calendar.domain.entities import CalendarEvent, Category, UserCalendar
from user_calendar.domain.value_objects import (
    CalendarId,
    CalendarProvider,
    CategoryId,
    CreatedAt,
    EventId,
    UserId,
)


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
        except ObjectDoesNotExist:
            return None

        return UserCalendar(
            calendar_id=CalendarId(model.calendar_id),
            user_id=UserId(model.user_id),
            provider=CalendarProvider(model.provider),
            created_at=CreatedAt(model.created_at),
            google_calendar_id=model.google_calendar_id,
            access_token=model.access_token,
            refresh_token=model.refresh_token,
        )

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

class DjangoCategoryRepository(CategoryRepository):
    def save(self, category: Category) -> None:
        CategoryModel.objects.update_or_create(
            category_id=category.category_id,
            defaults={
                "user_id": category.user_id,
                "name": category.name,
                "color": category.color,
                "estimated_monthly_cost": category.estimated_monthly_cost,
                "created_at": category.created_at.value,
            },
        )

    def find_by_user_id(self, user_id: int) -> List[Category]:
        rows = CategoryModel.objects.filter(user_id=user_id.value).order_by("created_at")
        return [
            Category(
                category_id=CategoryId(r.category_id),
                user_id=UserId(r.user_id),
                name=r.name,
                color=r.color,
                estimated_monthly_cost=r.estimated_monthly_cost,
                created_at=CreatedAt(r.created_at),
            )
            for r in rows
        ]
    
    def find_by_id(self, category_id: CategoryId) -> Optional[Category]:
        try:
            r = CategoryModel.objects.get(category_id=category_id.value)
        except ObjectDoesNotExist:
            return None

        return Category(
            category_id=CategoryId(r.category_id),
            user_id=UserId(r.user_id),
            name=r.name,
            color=r.color,
            estimated_monthly_cost=r.estimated_monthly_cost,
            created_at=CreatedAt(r.created_at),
        )

    def delete(self, category_id) -> None:
        CategoryModel.objects.filter(category_id=category_id).delete()

class DjangoCalendarEventRepository(CalendarEventRepository):
    def save(self, event: CalendarEvent) -> None:
        CalendarEventModel.objects.update_or_create(
            event_id=event.event_id.value,
            defaults={
                "user_id": event.user_id.value,
                "title": event.title,
                "start_at": event.start_at,
                "end_at": event.end_at,
                "estimated_cost": event.estimated_cost,
                "category_ids": [cid.value for cid in event.category_ids],
                "created_at": event.created_at.value,
            },
        )

    def find_by_user_id(self, user_id: UserId) -> List[CalendarEvent]:
        rows = CalendarEventModel.objects.filter(user_id=user_id.value).order_by("start_at")
        return [
            CalendarEvent(
                event_id=EventId(r.event_id),
                user_id=UserId(r.user_id),
                title=r.title,
                start_at=r.start_at,
                end_at=r.end_at,
                created_at=CreatedAt(r.created_at),
                estimated_cost=r.estimated_cost,
                category_ids=[CategoryId(UUID(x)) for x in (r.category_ids or [])],
            )
            for r in rows
        ]

    def find_by_id(self, event_id: EventId) -> Optional[CalendarEvent]:
        try:
            r = CalendarEventModel.objects.get(event_id=event_id.value)
        except ObjectDoesNotExist:
            return None

        return CalendarEvent(
            event_id=EventId(r.event_id),
            user_id=UserId(r.user_id),
            title=r.title,
            start_at=r.start_at,
            end_at=r.end_at,
            created_at=CreatedAt(r.created_at),
            estimated_cost=r.estimated_cost,
            category_ids=[CategoryId(UUID(x)) for x in (r.category_ids or [])],
        )

    def delete(self, event_id: EventId) -> None:
        CalendarEventModel.objects.filter(event_id=event_id.value).delete()
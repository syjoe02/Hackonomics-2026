from typing import Optional, List

from django.core.exceptions import ObjectDoesNotExist

from user_calendar.application.ports.repository import UserCalendarRepository, CategoryRepository
from user_calendar.domain.entities import UserCalendar, Category
from user_calendar.domain.value_objects import (CalendarId, CalendarProvider,
                                                CreatedAt, UserId)

from .models import UserCalendarModel, CategoryModel


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

class DjangoCategoryRepository(CategoryRepository):

    def save(self, category: Category) -> None:
        CategoryModel.objects.update_or_create(
            category_id=category.category_id,
            defaults={
                "user_id": category.user_id,
                "name": category.name,
                "color": category.color,
                "estimated_monthly_cost": category.estimated_monthly_cost,
            },
        )

    def find_by_user(self, user_id: int) -> List[Category]:
        models = CategoryModel.objects.filter(user_id=user_id.value)
        return [self._to_domain(m) for m in models]
    
    def find_by_id(self, category_id) -> Optional[Category]:
        try:
            model = CategoryModel.objects.get(category_id=category_id.value)
            return self._to_domain(model)
        except ObjectDoesNotExist:
            return None

    def delete(self, category_id) -> None:
        CategoryModel.objects.filter(category_id=category_id).delete()

    def _to_domain(self, model: CategoryModel) -> Category:
        return Category(
            category_id=model.category_id,
            user_id=model.user_id,
            name=model.name,
            color=model.color,
            estimated_monthly_cost=model.estimated_monthly_cost,
        )
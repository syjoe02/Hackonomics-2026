from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from user_calendar.domain.entities import CalendarEvent, Category, UserCalendar
from user_calendar.domain.value_objects import CalendarId, EventId, UserId


class UserCalendarRepository(ABC):

    @abstractmethod
    def save(self, calendar: UserCalendar) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_user_id(self, user_id: UserId) -> Optional[UserCalendar]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, calendar_id: CalendarId) -> Optional[UserCalendar]:
        raise NotImplementedError


class CategoryRepository(ABC):

    @abstractmethod
    def save(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[Category]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, category_id) -> Optional[Category]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, category_id) -> None:
        raise NotImplementedError


class CalendarEventRepository(ABC):

    @abstractmethod
    def save(self, event: CalendarEvent) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_user_id(self, user_id: UserId) -> List[CalendarEvent]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, event_id: EventId) -> Optional[CalendarEvent]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, event_id: EventId) -> None:
        raise NotImplementedError

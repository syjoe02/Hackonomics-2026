from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, List

from user_calendar.domain.entities import UserCalendar, Category, CalendarEvent
from user_calendar.domain.value_objects import CalendarId, UserId, EventId


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
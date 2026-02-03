from abc import ABC, abstractmethod
from typing import Optional

from user_calendar.domain.entities import UserCalendar
from user_calendar.domain.value_objects import CalendarId, UserId


class UserCalendarRepository(ABC):

    @abstractmethod
    def save(self, calendar: UserCalendar) -> None:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: UserId) -> Optional[UserCalendar]:
        pass

    @abstractmethod
    def find_by_id(self, calendar_id: CalendarId) -> Optional[UserCalendar]:
        pass

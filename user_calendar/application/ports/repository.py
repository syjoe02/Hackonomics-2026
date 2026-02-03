from abc import ABC, abstractmethod
from typing import Optional, List

from user_calendar.domain.entities import UserCalendar, Category
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

class CategoryRepository(ABC):

    @abstractmethod
    def save(self, category: Category) -> None:
        pass

    @abstractmethod
    def find_by_user(self, user_id: int) -> List[Category]:
        pass

    @abstractmethod
    def find_by_id(self, category_id) -> Optional[Category]:
        pass

    @abstractmethod
    def delete(self, category_id) -> None:
        pass
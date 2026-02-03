from common.errors.error_codes import ErrorCode
from common.errors.exceptions import BusinessException

from user_calendar.application.ports.repository import UserCalendarRepository
from user_calendar.domain.entities import UserCalendar
from user_calendar.domain.value_objects import CalendarId, UserId


class UserCalendarService:
    def __init__(self, repository: UserCalendarRepository):
        self.repository = repository

    def get_or_create_calendar_for_user(self, user_id: UserId) -> UserCalendar:
        calendar = self.repository.find_by_user_id(user_id)

        if calendar is None:
            calendar = UserCalendar.create_for_user(user_id)
            self.repository.save(calendar)

        return calendar

    def get_calendar(self, user_id: UserId) -> UserCalendar:
        calendar = self.repository.find_by_user_id(user_id)

        if calendar is None:
            raise BusinessException(
                ErrorCode.USER_CALENDAR_NOT_FOUND,
                f"UserCalendar not found for user_id={user_id.value}",
            )

        return calendar

    def connect_google_calendar(
        self,
        user_id: UserId,
        google_calendar_id: str,
        access_token: str,
        refresh_token: str,
    ) -> UserCalendar:
        calendar = self.repository.find_by_user_id(user_id)

        if calendar is None:
            raise BusinessException(
                ErrorCode.USER_CALENDAR_NOT_FOUND,
                f"Cannot connect Google Calendar. No calendar exists for user_id={user_id.value}",
            )

        # Domain behavior
        calendar.connect_google_calendar(
            google_calendar_id=google_calendar_id,
            access_token=access_token,
            refresh_token=refresh_token,
        )
        self.repository.save(calendar)
        return calendar

    def find_by_calendar_id(self, calendar_id: CalendarId) -> UserCalendar:
        calendar = self.repository.find_by_id(calendar_id)

        if calendar is None:
            raise BusinessException(
                ErrorCode.USER_CALENDAR_NOT_FOUND,
                f"UserCalendar not found for calendar_id={calendar_id.value}",
            )
        return calendar

from dataclasses import dataclass, field
from typing import Optional, List

from .value_objects import CalendarId, UserId, CalendarProvider, CreatedAt
from .events import UserCalendarCreated, UserCalendarConnected


@dataclass
class UserCalendar:
    # Aggregate Root - 1 user : 1 calendar
    calendar_id: CalendarId
    user_id: UserId
    provider: CalendarProvider
    created_at: CreatedAt

    google_calendar_id: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None

    @staticmethod
    def create_for_user(user_id: UserId) -> "UserCalendar":
        calendar = UserCalendar(
            calendar_id=CalendarId.new(),
            user_id=user_id,
            provider=CalendarProvider.google(),
            created_at=CreatedAt.now(),
        )

        calendar._raise_event(
            UserCalendarCreated(
                calendar_id=calendar.calendar_id.value,
                user_id=user_id.value,
            )
        )

        return calendar

    def connect_google_calendar(self, google_calendar_id: str, access_token: str, refresh_token: str):
        self.google_calendar_id = google_calendar_id
        self.access_token = access_token
        self.refresh_token = refresh_token

        self._raise_event(
            UserCalendarConnected(
                calendar_id=self.calendar_id.value,
                user_id=self.user_id.value,
                google_calendar_id=google_calendar_id,
            )
        )

    _events: List[object] = field(default_factory=list, init=False, repr=False)

    def _raise_event(self, event):
        self._events.append(event)

    def pull_events(self) -> List[object]:
        events = self._events
        self._events = []
        return events
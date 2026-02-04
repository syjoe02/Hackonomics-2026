from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserCalendarCreated:
    calendar_id: UUID
    user_id: int


@dataclass
class UserCalendarConnected:
    calendar_id: UUID
    user_id: int
    google_calendar_id: str


@dataclass
class CalendarEventCreated:
    event_id: UUID
    user_id: int
    title: str

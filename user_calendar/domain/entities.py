from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
from decimal import Decimal
from datetime import datetime, timezone
from uuid import UUID, uuid4

from .events import UserCalendarConnected, UserCalendarCreated, CalendarEventCreated
from .value_objects import CalendarId, CalendarProvider, CreatedAt, UserId, EventId, CategoryId


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

    _events: List[object] = field(default_factory=list, init=False, repr=False)

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

    def connect_google_calendar(
        self, google_calendar_id: str, access_token: str, refresh_token: str
    ):
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

    def _raise_event(self, event):
        self._events.append(event)

    def pull_events(self) -> List[object]:
        events = self._events
        self._events = []
        return events

@dataclass
class Category:
    category_id: CategoryId
    user_id: UserId
    name: str
    color: str
    estimated_monthly_cost: Decimal
    created_at: CreatedAt

    @staticmethod
    def create(
        user_id: UserId,
        name: str,
        color: str,
        estimated_monthly_cost: Decimal,
    ):
        return Category(
            category_id=uuid4(),
            user_id=user_id,
            name=name,
            color=color,
            estimated_monthly_cost=estimated_monthly_cost,
            created_at=CreatedAt.now(),
        )

@dataclass
class CalendarEvent:
    # Aggregate Root
    event_id: EventId
    user_id: UserId
    title: str
    start_at: datetime
    end_at: datetime
    created_at: CreatedAt

    estimated_cost: Optional[Decimal] = None
    category_ids: List[CategoryId] = field(default_factory=list)

    _events: List[object] = field(default_factory=list, init=False, repr=False)

    @staticmethod
    def create(
        user_id: UserId,
        title: str,
        start_at: datetime,
        end_at: datetime,
        estimated_cost: Optional[Decimal] = None,
        category_ids: Optional[List[CategoryId]] = None,
    ) -> "CalendarEvent":

        event = CalendarEvent(
            event_id=EventId.new(),
            user_id=user_id,
            title=title,
            start_at=start_at,
            end_at=end_at,
            created_at=CreatedAt.now(),
            estimated_cost=estimated_cost,
            category_ids=category_ids or [],
        )

        event._raise_event(
            CalendarEventCreated(
                event_id=event.event_id.value,
                user_id=user_id.value,
                title=title,
            )
        )
        return event
    
    def _raise_event(self, event: object) -> None:
        self._events.append(event)

    def pull_events(self) -> List[object]:
        events = self._events
        self._events = []
        return events

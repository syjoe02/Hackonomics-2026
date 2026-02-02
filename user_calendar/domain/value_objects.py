from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class CalendarId:
    value: UUID

    @staticmethod
    def new():
        return CalendarId(uuid4())


@dataclass(frozen=True)
class UserId:
    value: int


@dataclass(frozen=True)
class CalendarProvider:
    value: str  # "google"

    @staticmethod
    def google():
        return CalendarProvider("google")


@dataclass(frozen=True)
class CreatedAt:
    value: datetime

    @staticmethod
    def now():
        return CreatedAt(datetime.utcnow())
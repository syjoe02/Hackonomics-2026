from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from common.errors.error_codes import ErrorCode
from common.errors.exceptions import BusinessException
from user_calendar.application.ports.repository import (
    CalendarEventRepository, CategoryRepository)
from user_calendar.domain.entities import CalendarEvent
from user_calendar.domain.value_objects import CategoryId, EventId, UserId


class CalendarEventService:
    def __init__(
        self,
        event_repo: CalendarEventRepository,
        category_repo: CategoryRepository,
    ):
        self.event_repo = event_repo
        self.category_repo = category_repo

    def create_event(
        self,
        user_id: UserId,
        title: str,
        start_at: datetime,
        end_at: datetime,
        estimated_cost: Optional[Decimal],
        category_ids: List[UUID],
    ) -> CalendarEvent:
        if not title or not title.strip():
            raise BusinessException(ErrorCode.INVALID_PARAMETER)

        if end_at <= start_at:
            raise BusinessException(ErrorCode.INVALID_PARAMETER)

        domain_category_ids: List[CategoryId] = []
        for cid in category_ids:
            cat = self.category_repo.find_by_id(CategoryId(cid))
            if cat is None or cat.user_id.value != user_id.value:
                raise BusinessException(ErrorCode.FORBIDDEN)
            domain_category_ids.append(cat.category_id)

        event = CalendarEvent.create(
            user_id=user_id,
            title=title,
            start_at=start_at,
            end_at=end_at,
            estimated_cost=estimated_cost,
            category_ids=domain_category_ids,
        )
        self.event_repo.save(event)
        return event

    def list_events(self, user_id: UserId) -> List[CalendarEvent]:
        return self.event_repo.find_by_user_id(user_id)

    def delete_event(self, event_id: EventId, user_id: UserId) -> None:
        existing = self.event_repo.find_by_id(event_id)
        if existing is None:
            raise BusinessException(ErrorCode.DATA_NOT_FOUND)
        if existing.user_id.value != user_id.value:
            raise BusinessException(ErrorCode.FORBIDDEN)
        self.event_repo.delete(event_id)

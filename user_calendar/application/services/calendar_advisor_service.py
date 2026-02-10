import json

from common.errors.error_codes import ErrorCode
from common.errors.exceptions import BusinessException
from user_calendar.application.ports.external.calendar_advisor import (
    CalendarAdvisorPort,
)
from user_calendar.application.ports.repository import CalendarEventRepository
from user_calendar.domain.value_objects import UserId
from user_calendar.presentation.serializers import CalendarEventSerializer


class CalendarAdvisorService:
    def __init__(
        self,
        event_repo: CalendarEventRepository,
        advisor: CalendarAdvisorPort,
    ):
        self.event_repo = event_repo
        self.advisor = advisor

    def analyze_document_and_suggest(
        self,
        user_id: UserId,
        document_text: str,
    ) -> str:
        if not document_text:
            raise BusinessException(ErrorCode.INVALID_PARAMETER)

        events = self.event_repo.find_by_user_id(user_id)
        if not events:
            raise BusinessException(ErrorCode.DATA_NOT_FOUND)

        serialized_events = [
            CalendarEventSerializer.from_domain(e).data for e in events
        ]
        events_text = json.dumps(serialized_events, indent=2, ensure_ascii=False)

        return self.advisor.analyze_events(events_text, document_text)

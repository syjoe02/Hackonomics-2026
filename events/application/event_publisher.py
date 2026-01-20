from events.domain.entities import DomainEvent
from events.application.ports.event_repository import EventRepository

class EventPublisher:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    def publish(self, aggregate_type: str, aggregate_id: str, event_type: str, payload: dict):
        event = DomainEvent(
            aggregate_type=aggregate_type,
            aggregate_id=str(aggregate_id),
            event_type=event_type,
            payload=payload,
        )
        self.repository.save(event)
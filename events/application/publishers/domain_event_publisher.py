from events.domain.entities import DomainEvent

class DomainEventPublisher:
    def __init__(self, repository):
        self.repository = repository

    def publish(self, *, aggregate_type, aggregate_id, event_type, payload):
        event = DomainEvent(
            aggregate_type=aggregate_type,
            aggregate_id=str(aggregate_id),
            event_type=event_type,
            payload=payload,
        )
        self.repository.save(event)
from accounts.application.ports.event_publisher import (
    DomainEventPublisher as AccountPort,
)
from events.application.publishers.domain_event_publisher import (
    DomainEventPublisher as CorePublisher,
)
from events.domain.entities import DomainEvent


class AccountDomainEventPublisher(AccountPort):
    def __init__(self, outbox_repository):
        self.publisher = CorePublisher(outbox_repository)

    def publish(self, *, aggregate_type, aggregate_id, event_type, payload):
        event = DomainEvent(
            aggregate_type=aggregate_type,
            aggregate_id=str(aggregate_id),
            event_type=event_type,
            payload=payload,
        )

        self.publisher.publish(event)

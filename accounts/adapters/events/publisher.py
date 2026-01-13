from events.infra.outbox_models import OutboxEvent
from accounts.application.ports.event_publisher import DomainEventPublisher

class OutboxEventAdapter(DomainEventPublisher):
    def publish(self, event_type: str, payload: dict) -> None:
        OutboxEvent.objects.create(
            event_type=event_type,
            payload=payload,
        )
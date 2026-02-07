from events.application.ports.event_repository import EventRepository
from events.domain.entities import DomainEvent
from events.infra.kafka.producer import KafkaEventProducer


class KafkaEventRepository(EventRepository):
    def save(self, event: DomainEvent) -> None:
        producer = KafkaEventProducer()

        # Convert DomainEvent → Kafka message
        kafka_payload = {
            "event_id": event.event_id,
            "aggregate_type": event.aggregate_type,
            "aggregate_id": event.aggregate_id,
            "event_type": event.event_type,
            "occurred_at": event.occurred_at.isoformat(),
            "payload": event.payload,
        }

        producer.publish(
            topic="domain-events",
            event=kafka_payload,
        )

from events.infra.outbox_models import OutboxEvent
from events.infra.kafka.producer import KafkaEventProducer

def process_outbox():
    producer = KafkaEventProducer()
    events = OutboxEvent.objects.filter(published=False)

    for event in events:
        producer.publish(
            topic="domain-events",
            event={
                "aggregate_type": event.aggregate_type,
                "aggregate_id": event.aggregate_id,
                "event_type": event.event_type,
                "payload": event.payload,
                "created_at": event.created_at.isoformat(),
            }
        )
        event.published = True
        event.save(update_fields=["published"])
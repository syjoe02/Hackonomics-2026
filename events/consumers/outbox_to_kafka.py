from events.infra.outbox_models import OutboxEvent
from events.infra.kafka.producer import KafkaEventProducer
from django.db import transaction

TOPIC = "account-events"

def process_outbox_events():
    producer = KafkaEventProducer()
    events = OutboxEvent.objects.filter(published=False).order_by("created_at")[:100]

    for event in events:
        message = {
            "event_id": event.event_id,
            "aggregate_type": event.aggregate_type,
            "aggregate_id": event.aggregate_id,
            "event_type": event.event_type,
            "payload": event.payload,
            "created_at": event.created_at.isoformat(),
        }

        try:
            producer.publish(TOPIC, message)

            # Sending data using Kafka -> published=True
            with transaction.atomic():
                event.published = True
                event.save(update_fields=["published"])

        except Exception as e:
            print(f"Kafka publish failed: {e}")
            break
import time
import signal
from django.db import transaction

from events.infra.outbox_models import OutboxEvent
from events.infra.kafka.producer import KafkaEventProducer

TOPIC = "account-events"
RUNNING = True

# Loop
def shutdown_handler(sig, frame):
    global RUNNING
    RUNNING = False
    print("Shutting down outbox worker...")

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

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

# polling interval is 1s
def run_worker():
    print("Outbox worker started...")
    while RUNNING:
        process_outbox_events()
        time.sleep(1)
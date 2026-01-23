import json

from django.conf import settings
from kafka import KafkaConsumer

from accounts.application.usecases.event_router import AccountEventRouter


def start_kafka_consumer():
    consumer = KafkaConsumer(
        "account-events",
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="accounts-service",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )

    router = AccountEventRouter()
    print("Kafka Account Consumer started...")

    try:
        for message in consumer:
            event = message.value
            print("Received event:", event)
            router.route(event)
    except KeyboardInterrupt:
        print("Kafka consumer stopped.")
    finally:
        consumer.close()

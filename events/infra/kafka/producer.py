import json
from kafka import KafkaProducer
from django.conf import settings

class KafkaEventProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def publish(self, topic: str, event: dict):
        self.producer.send(topic, event)
        self.producer.flush()
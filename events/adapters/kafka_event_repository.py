from application.ports.event_repository import EventRepository
from events.infra.kafka.producer import KafkaEventProducer

class KafkaEventRepository(EventRepository):
    def save(self, event: dict):
        producer = KafkaEventProducer()
        producer.publish(topic="domain-events", event=event)
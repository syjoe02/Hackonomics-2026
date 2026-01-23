from abc import ABC, abstractmethod


class DomainEventPublisher(ABC):
    @abstractmethod
    def publish(self, *, aggregate_type, aggregate_id, event_type, payload):
        pass

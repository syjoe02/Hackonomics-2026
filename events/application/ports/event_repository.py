from abc import ABC, abstractmethod

from events.domain.entities import DomainEvent


class EventRepository(ABC):

    @abstractmethod
    def save(self, event: DomainEvent):
        pass

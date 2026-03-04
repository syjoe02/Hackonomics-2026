from events.domain.entities import DomainEvent


class DomainEventPublisher:
    def __init__(self, repository):
        self.repository = repository

    def publish(self, event: DomainEvent) -> None:
        self.repository.save(event)

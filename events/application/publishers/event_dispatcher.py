from events.application.publishers.handlers.user_event_publisher import UserEventPublisher
from events.domain.entities import DomainEvent

class EventDispatcher:
    def __init__(self, repository):
        self.repository = repository
        self.user_publisher = UserEventPublisher()

    def publish_user_signup(self, user):
        data = self.user_publisher.user_signup(user)

        event = DomainEvent(
            aggregate_type=data["aggregate_type"],
            aggregate_id=str(data["aggregate_id"]),
            event_type=data["event_type"],
            payload=data["payload"],
        )
        self.repository.save(event)
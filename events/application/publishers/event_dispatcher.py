from events.application.publishers.domain_event_publisher import DomainEventPublisher
from events.application.publishers.handlers.user_event_publisher import (
    UserEventPublisher,
)


class EventDispatcher:
    def __init__(self, repository):
        self.event_publisher = DomainEventPublisher(repository)

    def publish_user_signup(self, user):
        event = UserEventPublisher.user_signed_up(user)
        self.event_publisher.publish(event)

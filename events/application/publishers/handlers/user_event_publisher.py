from events.domain.entities import DomainEvent


class UserEventPublisher:

    @staticmethod
    def user_signed_up(user) -> DomainEvent:
        return DomainEvent(
            aggregate_type="User",
            aggregate_id=str(user.id),
            event_type="USER_SIGNUP",
            payload={
                "user_id": user.id,
                "email": user.email,
            },
        )

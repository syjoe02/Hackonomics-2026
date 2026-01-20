class UserEventPublisher:

    def user_signup(self, user):
        return {
            "aggregate_type": "User",
            "aggregate_id": user.id,
            "event_type": "USER_SIGNUP",
            "payload": {
                "user_id": user.id,
                "email": user.email,
            }
        }
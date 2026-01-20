from accounts.application.usecases.handlers.account_event_handler import AccountEventHandler

class AccountEventRouter:
    def __init__(self):
        self.handlers = {
            "USER_SIGNUP": AccountEventHandler(),
        }

    def route(self, event: dict):
        event_type = event.get("event_type")
        handler = self.handlers.get(event_type)

        if not handler:
            print(f"[WARN] No handler registered for event type: {event_type}")
            return

        handler.handle(event)
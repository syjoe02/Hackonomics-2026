class AccountEventRouter:
    def __init__(self):
        self.handlers = {}

    def route(self, event: dict):
        print("[INFO] Account service does not consume its own events.")

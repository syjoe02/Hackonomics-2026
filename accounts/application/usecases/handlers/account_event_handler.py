from django.db import transaction
from django.db import transaction, IntegrityError

from accounts.adapters.orm.models import AccountModel

class AccountEventHandler:
    def handle(self, event: dict):
        if event["event_type"] == "USER_SIGNUP":
            self.handle_user_signup(event["payload"])

    def handle_user_signup(self, payload: dict):
        print(f"Creating account for {payload['email']}")

        try:
            with transaction.atomic():
                account = AccountModel.objects.create(
                    user_id=payload["user_id"],
                    email=payload["email"],
                )
                print(f"Account created in DB: {account.id}")
        except IntegrityError:
            print(f"Account already exists for user {payload['email']}")

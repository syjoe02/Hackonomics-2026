from django.contrib.auth import get_user_model

User = get_user_model()

class DjangoUserRepository:
    def find_by_id(self, user_id: int):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def find_by_email(self, email: str):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
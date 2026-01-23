from django.contrib.auth import get_user_model

User = get_user_model()


# Using Django User model
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


# for field in User._meta.fields:
#     print(field.name, field.get_internal_type())
#
# id AutoField
# password CharField
# last_login DateTimeField
# is_superuser BooleanField
# username CharField
# first_name CharField
# last_name CharField
# email CharField
# is_staff BooleanField
# is_active BooleanField
# date_joined DateTimeField
#

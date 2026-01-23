from django.contrib.auth.models import User
from django.db import IntegrityError

from common.errors.error_codes import ErrorCode
from common.errors.exceptions import BusinessException


class SignupService:
    def signup(self, email: str, password: str) -> User:
        try:
            return User.objects.create_user(
                username=email,
                email=email,
                password=password,
            )
        except IntegrityError:
            raise BusinessException(ErrorCode.DUPLICATE_ENTRY)

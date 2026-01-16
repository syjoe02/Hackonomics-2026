from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from authentication.adapters.django.auth_service import CentralAuthAdapter
from common.errors.exceptions import BusinessException
from common.errors.error_codes import ErrorCode

class LoginService:
    def __init__(self):
        self.central_auth = CentralAuthAdapter()

    def login(self, email: str, password: str, device_id: str, remember_me: bool) -> dict:
        user = authenticate(username=email, password=password)
        if user is None:
            raise BusinessException(ErrorCode.INVALID_CREDENTIALS)

        try:
            return self.central_auth.login(
                user_id=str(user.id),
                device_id=device_id,
                remember_me=remember_me,
            )
        except Exception:
            raise BusinessException(ErrorCode.EXTERNAL_API_FAILED)

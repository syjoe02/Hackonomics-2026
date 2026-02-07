from django.contrib.auth import authenticate

from authentication.adapters.django.auth_service import CentralAuthAdapter
from common.errors.error_codes import ErrorCode
from common.errors.exceptions import BusinessException


class LoginService:
    def __init__(self) -> None:
        self.central_auth = CentralAuthAdapter()

    def login(
        self, email: str, password: str, device_id: str, remember_me: bool
    ) -> dict:
        user = authenticate(username=email, password=password)

        if user is None:
            raise BusinessException(ErrorCode.INVALID_CREDENTIALS)

        user_id = str(user.pk)

        try:
            return self.central_auth.login(
                user_id=user_id,
                device_id=device_id,
                remember_me=remember_me,
            )
        except BusinessException:
            raise
        except Exception:
            raise BusinessException(ErrorCode.EXTERNAL_API_FAILED)

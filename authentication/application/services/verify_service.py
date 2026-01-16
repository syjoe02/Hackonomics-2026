from authentication.adapters.django.auth_service import CentralAuthAdapter
from common.errors.exceptions import BusinessException
from common.errors.error_codes import ErrorCode

class VerifyService:
    def __init__(self):
        self.central_auth = CentralAuthAdapter()

    def verify(self, access_token: str) -> dict:
        if not access_token:
            raise BusinessException(ErrorCode.UNAUTHORIZED)

        try:
            return self.central_auth.verify(access_token)
        except Exception:
            raise BusinessException(ErrorCode.TOKEN_INVALID)
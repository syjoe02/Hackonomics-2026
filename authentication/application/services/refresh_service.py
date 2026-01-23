from authentication.adapters.django.auth_service import CentralAuthAdapter
from common.errors.error_codes import ErrorCode
from common.errors.exceptions import BusinessException


class RefreshService:
    def __init__(self):
        self.central_auth = CentralAuthAdapter()

    def refresh(self, refresh_token: str) -> dict:
        if not refresh_token:
            raise BusinessException(ErrorCode.REFRESH_TOKEN_MISSING)

        try:
            return self.central_auth.refresh(refresh_token)
        except Exception:
            raise BusinessException(ErrorCode.REFRESH_TOKEN_INVALID)

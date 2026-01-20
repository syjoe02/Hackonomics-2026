from authentication.adapters.django.auth_service import CentralAuthAdapter
from authentication.adapters.orm.repository import DjangoUserRepository
from common.errors.exceptions import BusinessException
from common.errors.error_codes import ErrorCode

class VerifyService:
    def __init__(self):
        self.central_auth = CentralAuthAdapter()
        self.user_repository = DjangoUserRepository()

    def verify(self, access_token: str) -> dict:
        if not access_token:
            raise BusinessException(ErrorCode.UNAUTHORIZED)

        try:
            payload = self.central_auth.verify(access_token)
        except Exception:
            raise BusinessException(ErrorCode.TOKEN_INVALID)
    
        user_id = payload.get("user_id")
        if not user_id:
            raise BusinessException(ErrorCode.UNAUTHORIZED)

        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise BusinessException(ErrorCode.USER_NOT_FOUND)

        return {
            "user_id": user.id,
            "email": user.email,
            "device_id": payload.get("device_id"),
            "exp": payload.get("exp"),
        }

    
from django.contrib.auth.models import User

from authentication.adapters.django.auth_service import CentralAuthAdapter
from authentication.adapters.django.google_oauth import GoogleOAuthAdapter
from common.errors.error_codes import ErrorCode
from common.errors.exceptions import BusinessException


class OAuthService:
    def __init__(self):
        self.google_adapter = GoogleOAuthAdapter()
        self.central_auth = CentralAuthAdapter()

    def google_login(self, code: str) -> dict:
        try:
            token_data = self.google_adapter.exchange_code_for_token(code)
            userinfo = self.google_adapter.get_userinfo(token_data["access_token"])
        except Exception:
            raise BusinessException(ErrorCode.GOOGLE_AUTH_FAILED)

        email = userinfo.get("email")
        if not email:
            raise BusinessException(ErrorCode.INVALID_PARAMETER)

        user, _ = User.objects.get_or_create(username=email, defaults={"email": email})

        try:
            return self.central_auth.login(
                user_id=str(user.id),
                device_id="google-oauth",
                remember_me=True,
            )
        except Exception:
            raise BusinessException(ErrorCode.EXTERNAL_API_FAILED)

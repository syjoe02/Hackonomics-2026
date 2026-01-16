from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError

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
    
    def googleLogin(self, email: str) -> dict:
        user, _ = User.objects.get_or_create(
            username=email,
            defaults={"email": email}
        )

        try:
            return self.central_auth.login(
                user_id=str(user.id),
                device_id="google-oauth",
                remember_me=True,
            )
        except Exception:
            raise BusinessException(ErrorCode.EXTERNAL_API_FAILED)

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
        
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError

from authentication.adapters.django.auth_service import CentralAuthAdapter

class LoginService:
    def __init__(self):
        self.central_auth = CentralAuthAdapter()

    def login(self, email: str, password: str, device_id: str, remember_me: bool) -> dict:
        user = authenticate(username=email, password=password)
        if user is None:
            raise ValueError("Invalid credentials")
        try:
            tokens = self.central_auth.login(
                user_id=str(user.id),
                device_id=device_id,
                remember_me=remember_me,
            )
        except Exception as e:
            raise ValueError(f"Central-Auth connection failed: {str(e)}")
        
        return tokens

class SignupService:
    def signup(self, email: str, password: str) -> User:
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
            )
        except IntegrityError:
            raise ValueError("Email already exists")
        return user
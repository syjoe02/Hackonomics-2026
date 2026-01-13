from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError

class LoginService:
    def login(self, request, email: str, password: str) -> User:
        user = authenticate(
            request,
            username=email,
            password=password,
        )
        if user is None:
            raise ValueError("Invalid credentials")
        return user

class SignupService:
    def signup(self, email: str, username: str, password: str) -> User:
        try:
            user = User.objects.create_user(
                email=email,
                username=username,
                password=password,
            )
        except IntegrityError:
            raise ValueError("Email already exists")
        return user
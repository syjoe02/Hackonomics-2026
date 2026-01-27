from types import SimpleNamespace

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from authentication.application.services.authentication_service import \
    AuthenticationService


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        skip_paths = [
            "/api/auth/login/",
            "/api/auth/signup/",
            "/api/auth/refresh/",
        ]
        if any(request.path.startswith(p) for p in skip_paths):
            return None

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            print("NO AUTH HEADER")
            return None

        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                return None
        except ValueError:
            raise AuthenticationFailed("Invalid Authorization header format")

        service = AuthenticationService()
        payload = service.verify(token)

        # Payload data
        user = SimpleNamespace(
            id=payload["user_id"],
            email=payload.get("email"),
            is_authenticated=True,
            payload=payload,
        )

        return user, token

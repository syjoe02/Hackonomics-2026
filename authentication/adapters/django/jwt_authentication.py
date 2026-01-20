from types import SimpleNamespace
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from authentication.application.services.authentication_service import AuthenticationService

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print("JWTAuthentication.authenticate called")

        auth_header = request.headers.get("Authorization")
        print("AUTH HEADER:", auth_header)

        if not auth_header:
            print("NO AUTH HEADER")
            return None

        try:
            scheme, token = auth_header.split()
            print("SCHEME:", scheme)
            print("TOKEN:", token)
            if scheme.lower() != "bearer":
                print("NOT BEARER")
                return None
        except ValueError:
            print("HEADER SPLIT ERROR")
            raise AuthenticationFailed("Invalid Authorization header format")

        service = AuthenticationService()
        payload = service.verify(token)

        print("JWT PAYLOAD:", payload)
        
        user = SimpleNamespace(
            id=payload["user_id"],
            email=payload.get("email"),
            is_authenticated=True,
            payload=payload,
        )

        return user, token
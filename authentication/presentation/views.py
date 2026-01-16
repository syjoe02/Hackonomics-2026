
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from authentication.presentation.serializers import (
    LoginRequestSerializer,
    SignupRequestSerializer,
)
from authentication.adapters.django.google_oauth import GoogleOAuthAdapter
from authentication.application.services.authentication_service import AuthenticationService
from common.EmptySerializer import EmptySerializer
from common.errors.error_codes import ErrorCode
from common.errors.exceptions import BusinessException

class LoginAPIView(GenericAPIView):
    serializer_class = LoginRequestSerializer

    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_service = AuthenticationService()
        tokens = auth_service.login(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
            device_id=serializer.validated_data["device_id"],
            remember_me=serializer.validated_data.get("remember_me", False),
        )

        response = Response(
            {"access_token": tokens["access_token"]},
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh_token"],
            httponly=True,
            secure=settings.IS_PRODUCTION,
            samesite="Strict" if settings.IS_PRODUCTION else "Lax",
            max_age=60 * 60 * 24 * (30 if serializer.validated_data.get("remember_me") else 7),
            path="/"
        )
        return response

class GoogleLoginAPIView(APIView):
    def get(self, request):
        adapter = GoogleOAuthAdapter()
        return redirect(adapter.build_login_url())
    
class GoogleCallbackAPIView(APIView):
    def get(self, request):
        code = request.GET.get("code")
        if not code:
            raise BusinessException(ErrorCode.GOOGLE_AUTH_CODE_MISSING)

        # login
        auth_service = AuthenticationService()
        tokens = auth_service.google_login(code)
        # refresh token -> stored in Cookie
        response = redirect(f"{settings.FRONTEND_URL}/oauth/callback")
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh_token"],
            httponly=True,
            secure=settings.IS_PRODUCTION,
            samesite="Strict" if settings.IS_PRODUCTION else "Lax",
            path="/",
        )
        return response

class LogoutAPIView(GenericAPIView):
    serializer_class = EmptySerializer

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        auth_service = AuthenticationService()
        auth_service.logout(refresh_token)

        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(
            "refresh_token",
            samesite="Strict" if settings.IS_PRODUCTION else "Lax",
            path="/"
        )
        return response
    
class SignupAPIView(GenericAPIView):
    serializer_class = SignupRequestSerializer

    def post(self, request):
        serializer = SignupRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_service = AuthenticationService()
        user = auth_service.signup(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        return Response(
            {"id": user.id, "email": user.email,},
            status=status.HTTP_201_CREATED,
        )

class RefreshAPIView(GenericAPIView):
    serializer_class = EmptySerializer

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        auth_service = AuthenticationService()
        tokens = auth_service.refresh(refresh_token)

        return Response(
            {"access_token": tokens["access_token"]},
            status=status.HTTP_200_OK
        )

@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfAPIView(GenericAPIView):
    serializer_class = EmptySerializer

    def get(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class MeAPIView(GenericAPIView):
    serializer_class = EmptySerializer

    def get(self, request):
        access_token = request.headers.get("Authorization")

        auth_service = AuthenticationService()
        user_info = auth_service.verify(access_token)

        return Response(user_info, status=status.HTTP_200_OK)
        
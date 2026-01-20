
from django.db import transaction
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from authentication.presentation.serializers import (
    LoginRequestSerializer,
    SignupRequestSerializer,
)
from authentication.adapters.django.google_oauth import GoogleOAuthAdapter
from authentication.application.services.authentication_service import AuthenticationService
from common.EmptySerializer import EmptySerializer
from common.errors.error_codes import ErrorCode
from common.errors.exceptions import BusinessException
from events.application.publishers.event_dispatcher import EventDispatcher
from events.adapters.outbox_repository import OutboxEventRepository

class LoginAPIView(GenericAPIView):
    serializer_class = LoginRequestSerializer
    permission_classes = [AllowAny]

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

@extend_schema(exclude=True)
class GoogleLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        adapter = GoogleOAuthAdapter()
        return redirect(adapter.build_login_url())
    
@extend_schema(exclude=True)
class GoogleCallbackAPIView(APIView):
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_service = AuthenticationService()
        dispatcher = EventDispatcher(OutboxEventRepository())
        
        with transaction.atomic():
            user = auth_service.signup(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )

            # Publish event → Stored Outbox
            dispatcher.publish_user_signup(user)

        return Response(
            {
                "id": user.id,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )

class RefreshAPIView(GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        auth_service = AuthenticationService()
        tokens = auth_service.refresh(refresh_token)

        return Response(
            {"access_token": tokens["access_token"]},
            status=status.HTTP_200_OK
        )
    
class MeAPIView(GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "user_id": request.user.id,
                "email": request.user.email,
            },
            status=status.HTTP_200_OK,
        )

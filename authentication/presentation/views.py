import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
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
from common.EmptySerializer import EmptySerializer
from authentication.application.services import LoginService, SignupService

class LoginAPIView(GenericAPIView):
    serializer_class = LoginRequestSerializer

    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            tokens = LoginService().login(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
                device_id=serializer.validated_data["device_id"],
                remember_me=serializer.validated_data.get("remember_me", False),
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]

        response = Response(
            {"access_token": access_token},
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
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
        url = adapter.build_login_url()
        return redirect(url)
    
class GoogleCallbackAPIView(APIView):
    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return Response({"error": "Missing code"}, status=400)

        adapter = GoogleOAuthAdapter()
        # google code -> token
        token_data = adapter.exchange_code_for_token(code)
        access_token = token_data["access_token"]
        # token -> user info
        userinfo = adapter.get_userinfo(access_token)
        email = userinfo.get("email")
        # login
        tokens = LoginService().googleLogin(email)
        refresh_token = tokens["refresh_token"]
        # refresh token -> stored in Cookie
        response = redirect(f"{settings.FRONTEND_URL}/oauth/callback")

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
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

        if refresh_token:
            try:
                requests.post(
                    f"{settings.CENTRAL_AUTH_URL}/auth/logout",
                    headers={
                        "X-Service-Key": settings.CENTRAL_AUTH_SERVICE_KEY,
                        "Authorization": f"Bearer {refresh_token}",
                    },
                    timeout=settings.CENTRAL_AUTH_TIMEOUT,
                )
            except requests.RequestException:
                pass

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

        try:
            user = SignupService().signup(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"id": user.id, "email": user.email,},
            status=status.HTTP_201_CREATED,
        )

class RefreshAPIView(GenericAPIView):
    serializer_class = EmptySerializer

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"error": "no refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            res = requests.post(
                f"{settings.CENTRAL_AUTH_URL}/auth/refresh",
                headers={
                    "X-Service-Key": settings.CENTRAL_AUTH_SERVICE_KEY,
                    "Authorization": f"Bearer {refresh_token}",
                },
                timeout=settings.CENTRAL_AUTH_TIMEOUT,
            )
        except requests.RequestException:
            return Response({"error": "central auth unavailable"}, status=502)

        if res.status_code != 200:
            return Response({"error": "refresh failed"}, status=status.HTTP_401_UNAUTHORIZED)

        data = res.json()
        return Response({"access_token": data["access_token"]}, status=200)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfAPIView(GenericAPIView):
    serializer_class = EmptySerializer

    def get(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class MeAPIView(GenericAPIView):
    serializer_class = EmptySerializer

    def get(self, request):
        access_token = request.headers.get("Authorization")
        if not access_token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            res = requests.post(
                f"{settings.CENTRAL_AUTH_URL}/auth/verify",
                headers={
                    "X-Service-Key": settings.CENTRAL_AUTH_SERVICE_KEY,
                    "Authorization": access_token,
                },
                timeout=settings.CENTRAL_AUTH_TIMEOUT,
            )
        except requests.RequestException:
            return Response({"error": "central auth unavailable"}, status=502)

        if res.status_code != 200:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(res.json(), status=200)
        
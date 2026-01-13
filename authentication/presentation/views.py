from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from authentication.presentation.serializers import (
    LoginRequestSerializer,
    LoginResponseSerializer,
    SignupRequestSerializer,
    UserResponseSerializer,
)
from common.EmptySerializer import EmptySerializer
from authentication.application.services import LoginService, SignupService

class LoginAPIView(GenericAPIView):
    serializer_class = LoginRequestSerializer

    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try: 
            user = LoginService().login(
                request = request,
                email = serializer.validated_data["email"],
                password = serializer.validated_data["password"],
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
        login(request, user)

        return Response(
            LoginResponseSerializer(user).data,
            status=status.HTTP_200_OK,
        )

class LogoutAPIView(GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

class SignupAPIView(GenericAPIView):
    serializer_class = SignupRequestSerializer

    def post(self, request):
        serializer = SignupRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = SignupService().signup(
                email=serializer.validated_data["email"],
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"id": user.id, "email": user.email, "username": user.username,},
            status=status.HTTP_201_CREATED,
        )

@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfAPIView(GenericAPIView):
    serializer_class = EmptySerializer

    def get(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class MeAPIView(GenericAPIView):
    serializer_class = UserResponseSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        data = {"id": request.user.id, "email": request.user.email}
        return Response(UserResponseSerializer(data).data, status=status.HTTP_200_OK)
        
from django.urls import path
from authentication.presentation.views import (
    LoginAPIView,
    GoogleLoginAPIView,
    GoogleCallbackAPIView,
    LogoutAPIView,
    SignupAPIView,
    RefreshAPIView,
    MeAPIView,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view()),
    path("google/login/", GoogleLoginAPIView.as_view()),
    path("google/callback/", GoogleCallbackAPIView.as_view()),
    path("logout/", LogoutAPIView.as_view()),
    path("signup/", SignupAPIView.as_view()),
    path("refresh/", RefreshAPIView.as_view()),
    path("me/", MeAPIView.as_view()),
]
from django.urls import path
from authentication.presentation.views import (
    LoginAPIView,
    OAuthLoginAPIView,
    LogoutAPIView,
    SignupAPIView,
    RefreshAPIView,
    CsrfAPIView,
    MeAPIView,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view()),
    path("oauth/login", OAuthLoginAPIView.as_view()),
    path("logout/", LogoutAPIView.as_view()),
    path("signup/", SignupAPIView.as_view()),
    path("refresh/", RefreshAPIView.as_view()),
    path("csrf/", CsrfAPIView.as_view()),
    path("me/", MeAPIView.as_view()),
]
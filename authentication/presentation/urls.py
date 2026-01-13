from django.urls import path
from authentication.presentation.views import (
    LoginAPIView,
    LogoutAPIView,
    SignupAPIView,
    CsrfAPIView,
    MeAPIView,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view()),
    path("logout/", LogoutAPIView.as_view()),    
    path("signup/", SignupAPIView.as_view()),
    path("csrf/", CsrfAPIView.as_view()),
    path("me/", MeAPIView.as_view()),
]
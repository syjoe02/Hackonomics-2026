from django.urls import path

from user_calendar.presentation.views import (
    GoogleCalendarOAuthCallbackAPIView, GoogleCalendarOAuthLoginAPIView,
    MyCalendarAPIView, UserCalendarInitAPIView)

urlpatterns = [
    path("init/", UserCalendarInitAPIView.as_view(), name="calendar-init"),
    path(
        "oauth/login/",
        GoogleCalendarOAuthLoginAPIView.as_view(),
        name="calendar-oauth-login",
    ),
    path(
        "oauth/callback/",
        GoogleCalendarOAuthCallbackAPIView.as_view(),
        name="calendar-oauth-callback",
    ),
    path("me/", MyCalendarAPIView.as_view(), name="my-calendar"),
]

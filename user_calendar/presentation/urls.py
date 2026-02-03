from django.urls import path

from user_calendar.presentation.views import (
    GoogleCalendarOAuthCallbackAPIView, GoogleCalendarOAuthLoginAPIView,
    MyCalendarAPIView, UserCalendarInitAPIView, CategoryCreateAPIView, CategoryListAPIView, CategoryDeleteAPIView,)

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


    path("categories/create/", CategoryCreateAPIView.as_view()),
    path("categories/", CategoryListAPIView.as_view()),
    path("categories/<uuid:category_id>/", CategoryDeleteAPIView.as_view()),
]

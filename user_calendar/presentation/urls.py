from django.urls import path

from user_calendar.presentation.views import (
    CalendarAdviceView,
    CalendarEventCreateAPIView,
    CalendarEventDetailAPIView,
    CalendarEventListAPIView,
    CategoryCreateAPIView,
    CategoryDeleteAPIView,
    CategoryListAPIView,
    GoogleCalendarOAuthCallbackAPIView,
    GoogleCalendarOAuthLoginAPIView,
    MyCalendarAPIView,
    UserCalendarInitAPIView,
)

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
    # Categories
    path("categories/create/", CategoryCreateAPIView.as_view()),
    path("categories/", CategoryListAPIView.as_view()),
    path("categories/<uuid:category_id>/", CategoryDeleteAPIView.as_view()),
    # Calendar Events
    path("events/create/", CalendarEventCreateAPIView.as_view(), name="event-create"),
    path("events/", CalendarEventListAPIView.as_view(), name="event-list"),
    path(
        "events/<uuid:event_id>/",
        CalendarEventDetailAPIView.as_view(),
        name="event-detail",
    ),
    path(
        "advisor/",
        CalendarAdviceView.as_view(),
        name="calendar-advisor",
    ),
]

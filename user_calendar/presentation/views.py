import google_auth_oauthlib.flow
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user_calendar.adapters.orm.repository import DjangoUserCalendarRepository
from user_calendar.application.services.user_calendar_service import \
    UserCalendarService
from user_calendar.domain.value_objects import UserId
from user_calendar.presentation.serializers import UserCalendarSerializer
from user_calendar.utils.google_oauth import get_google_calendar_client_config


class UserCalendarInitAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        repo = DjangoUserCalendarRepository()
        service = UserCalendarService(repo)

        calendar = service.get_or_create_calendar_for_user(UserId(request.user.id))

        serializer = UserCalendarSerializer.from_domain(calendar)
        return Response(serializer.data, status=201)


class GoogleCalendarOAuthLoginAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            get_google_calendar_client_config(),
            scopes=["https://www.googleapis.com/auth/calendar"],
        )

        flow.redirect_uri = settings.GOOGLE_CALENDAR_REDIRECT_URI

        authorization_url, state = flow.authorization_url(
            access_type="offline", include_granted_scopes="true"
        )

        # Save state in session
        request.session["google_calendar_oauth_state"] = state

        return Response({"redirect_url": authorization_url})


class GoogleCalendarOAuthCallbackAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        state = request.session.get("google_calendar_oauth_state")

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            get_google_calendar_client_config(),
            scopes=["https://www.googleapis.com/auth/calendar"],
            state=state,
        )

        flow.redirect_uri = settings.GOOGLE_CALENDAR_REDIRECT_URI

        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials

        repo = DjangoUserCalendarRepository()
        service = UserCalendarService(repo)

        # Stored tokens in UserCalendar
        calendar = service.connect_google_calendar(
            user_id=UserId(request.user.id),
            google_calendar_id="primary",  # Default calendar
            access_token=credentials.token,
            refresh_token=credentials.refresh_token,
        )

        serializer = UserCalendarSerializer.from_domain(calendar)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyCalendarAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        repo = DjangoUserCalendarRepository()
        service = UserCalendarService(repo)

        calendar = service.get_calendar(UserId(request.user.id))

        serializer = UserCalendarSerializer.from_domain(calendar)
        return Response(serializer.data, status=200)

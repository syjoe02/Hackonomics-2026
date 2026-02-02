from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from user_calendar.domain.value_objects import UserId
from user_calendar.adapters.orm.repository import DjangoUserCalendarRepository
from user_calendar.presentation.serializers import (
    ConnectGoogleCalendarSerializer,
    UserCalendarSerializer,
)
from user_calendar.application.services.user_calendar_service import UserCalendarService

class UserCalendarInitAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        repo = DjangoUserCalendarRepository()
        service = UserCalendarService(repo)

        calendar = service.get_or_create_calendar_for_user(
            UserId(request.user.id)
        )

        serializer = UserCalendarSerializer.from_domain(calendar)
        return Response(serializer.data, status=201)
    
class ConnectGoogleCalendarAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ConnectGoogleCalendarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repo = DjangoUserCalendarRepository()
        service = UserCalendarService(repo)

        calendar = service.connect_google_calendar(
            user_id=UserId(request.user.id),
            google_calendar_id=serializer.validated_data["google_calendar_id"],
            access_token=serializer.validated_data["access_token"],
            refresh_token=serializer.validated_data["refresh_token"],
        )

        response_serializer = UserCalendarSerializer.from_domain(calendar)
        return Response(response_serializer.data, status=200)

class MyCalendarAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        repo = DjangoUserCalendarRepository()
        service = UserCalendarService(repo)

        calendar = service.get_calendar(UserId(request.user.id))

        serializer = UserCalendarSerializer.from_domain(calendar)
        return Response(serializer.data, status=200)

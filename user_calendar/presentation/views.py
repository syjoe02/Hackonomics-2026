import google_auth_oauthlib.flow
from django.conf import settings
from decimal import Decimal
from uuid import UUID
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user_calendar.adapters.orm.repository import DjangoUserCalendarRepository, DjangoCategoryRepository
from user_calendar.application.services.user_calendar_service import \
    UserCalendarService
from user_calendar.application.services.category_service import CategoryService
from user_calendar.domain.value_objects import UserId, CategoryId
from user_calendar.presentation.serializers import UserCalendarSerializer, CategorySerializer
from user_calendar.utils.google_oauth import build_google_calendar_flow


class UserCalendarInitAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        repo = DjangoUserCalendarRepository()
        service = UserCalendarService(repo)

        calendar = service.get_or_create_calendar_for_user(UserId(request.user.id))

        serializer = UserCalendarSerializer.from_domain(calendar)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GoogleCalendarOAuthLoginAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        flow = build_google_calendar_flow()
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

        flow = build_google_calendar_flow(state)

        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials

        repo = DjangoUserCalendarRepository()
        service = UserCalendarService(repo)

        # Stored tokens in UserCalendar
        existing_calendar = service.get_calendar(UserId(request.user.id))
        calendar = service.connect_google_calendar(
            user_id=UserId(request.user.id),
            google_calendar_id="primary",  # Default calendar
            access_token=credentials.token,
            refresh_token=credentials.refresh_token or existing_calendar.refresh_token,
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
        return Response(serializer.data, status=status.HTTP_200_OK)

# Categories
class CategoryCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        repo = DjangoCategoryRepository()
        service = CategoryService(repo)

        category = service.create_category(
            user_id=UserId(request.user.id),
            name=request.data["name"],
            color=request.data["color"],
            estimated_monthly_cost=Decimal(request.data["estimated_monthly_cost"]),
        )

        serializer = CategorySerializer.from_domain(category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        repo = DjangoCategoryRepository()
        service = CategoryService(repo)

        categories = service.list_categories(UserId(request.user.id))

        serializer = [CategorySerializer.from_domain(c).data for c in categories]
        return Response(serializer, status=status.HTTP_200_OK)


class CategoryDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, category_id: str):
        repo = DjangoCategoryRepository()
        service = CategoryService(repo)

        service.delete_category(CategoryId(UUID(category_id)))
        return Response(status=status.HTTP_204_NO_CONTENT)
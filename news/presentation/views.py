from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.adapters.orm.repository import DjangoAccountRepository
from news.adapters.gemini.business_news_adapter import GeminiBusinessNewsAdapter
from news.adapters.orm.repository import DjangoBusinessNewsRepository
from news.application.services.business_news_service import BusinessNewsService
from user_calendar.domain.value_objects import UserId


class BusinessNewsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = BusinessNewsService(
            account_repo=DjangoAccountRepository(),
            news_port=GeminiBusinessNewsAdapter(),
            news_repo=DjangoBusinessNewsRepository(),
        )

        data = service.get_user_business_news(UserId(request.user.id))

        return Response(data)

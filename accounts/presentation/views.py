from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from accounts.application.usecases import (
    GetAccountUseCase,
    UpdateAccountUseCase,
    GetExchangeRateUseCase,
)
from accounts.application.dto import AccountUpdateCommand
from accounts.adapters.orm.repository import DjangoAccountRepository
from accounts.adapters.events.publisher import OutboxEventAdapter
from accounts.presentation.serializers import AccountUpdateSerializer
from common.EmptySerializer import EmptySerializer
from exchange.application.services import ExchangeRateService

class AccountView(GenericAPIView):
    serializer_class = AccountUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usecase = GetAccountUseCase(
            repository = DjangoAccountRepository()
        )
        result = usecase.execute(user_id=request.user.id)
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AccountUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        command = AccountUpdateCommand(**serializer.validated_data)

        usecase = UpdateAccountUseCase(
            repository=DjangoAccountRepository(),
            event_publisher=OutboxEventAdapter(),
        )
        usecase.execute(
            user_id=request.user.id,
            command=command,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class MyExchangeRateAPIView(GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usecase = GetExchangeRateUseCase(
            repository=DjangoAccountRepository(),
            exchange_service=ExchangeRateService(),
        )
        
        result = usecase.execute(user_id=request.user.id)
        return Response(result, status=status.HTTP_200_OK)
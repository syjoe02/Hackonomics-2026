from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.adapters.events.event_publisher import \
    AccountDomainEventPublisher
from accounts.adapters.orm.repository import DjangoAccountRepository
from accounts.application.dto import AccountUpdateCommand
from accounts.application.usecases.get_account_usecase import GetAccountUseCase
from accounts.application.usecases.get_exchange_rate_usecase import \
    GetExchangeRateUseCase
from accounts.application.usecases.update_account_usecase import \
    UpdateAccountUseCase
from accounts.presentation.serializers import AccountUpdateSerializer
from common.EmptySerializer import EmptySerializer
from events.adapters.outbox_repository import OutboxEventRepository
from exchange.application.services import ExchangeRateService


class AccountView(GenericAPIView):
    serializer_class = AccountUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usecase = GetAccountUseCase(repository=DjangoAccountRepository())
        result = usecase.execute(user_id=request.user.id)
        if result is None:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AccountUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        command = AccountUpdateCommand(**serializer.validated_data)

        event_publisher = AccountDomainEventPublisher(
            outbox_repository=OutboxEventRepository(),
        )

        usecase = UpdateAccountUseCase(
            repository=DjangoAccountRepository(),
            event_publisher=event_publisher,
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

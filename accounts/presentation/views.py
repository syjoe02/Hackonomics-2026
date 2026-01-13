from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from accounts.application.usecases import UpdateAccountUseCase
from accounts.application.dto import AccountUpdateCommand
from accounts.adapters.orm.repository import DjangoAccountRepository
from accounts.adapters.events.publisher import OutboxEventAdapter
from accounts.presentation.serializers import AccountUpdateSerializer
from common.EmptySerializer import EmptySerializer
from exchange.application.services import ExchangeRateService

class AccountView(GenericAPIView):
    serializer_class = AccountUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AccountUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        command = AccountUpdateCommand(**serializer.validated_data)

        user_id = request.user.id

        usecase = UpdateAccountUseCase(
            repository=DjangoAccountRepository(),
            event_publisher=OutboxEventAdapter(),
        )
        usecase.execute(user_id=user_id, command=command)

        return Response({"status": "ok"})
    
class MyExchangeRateAPIView(GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        repo = DjangoAccountRepository()
        account = repo.find_by_user_id(request.user.id)

        if not account:
            return Response({"error": "Account not found"}, status=404)
        
        user_currency = account.country.currency.upper()

        try:
            rate = ExchangeRateService().get_usd_to_currency(user_currency)
        except ValidationError as e:
            raise ValidationError({"currency": str(e)})

        return Response({
            "base": "USD",
            "target": user_currency,
            "rate": rate,
        })
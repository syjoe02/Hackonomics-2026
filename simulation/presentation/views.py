from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from simulation.application.usecases.compare_investment_usecase import (
    CompareInvestmentUseCase
)
from exchange.application.services import ExchangeHistoryService
from accounts.adapters.orm.repository import DjangoAccountRepository

from common import EmptySerializer


class CompareDcaVsDepositAPIView(GenericAPIView):
    serializer_class = EmptySerializer

    def post(self, request):
        """
        Body:
        {
            "period": "1y" | "2y",
            "deposit_rate": 3.5
        }
        """
        user = request.user
        period = request.data.get("period", "1y")
        deposit_rate = request.data.get("deposit_rate")

        usecase = CompareInvestmentUseCase(
            account_repository=DjangoAccountRepository(),
            exchange_history_service=ExchangeHistoryService(),
        )

        result = usecase.execute(
            user_id=user.id,
            period=period,
            deposit_rate=float(deposit_rate),
        )

        return Response(result.to_dict(), status=status.HTTP_200_OK)
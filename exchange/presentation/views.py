from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError

from accounts.adapters.orm.repository import DjangoAccountRepository
from common.EmptySerializer import EmptySerializer
from exchange.application.services import ExchangeRateService
from exchange.presentation.serializers import ExchangeRateResponseSerializer
from exchange.application.services import ExchangeHistoryService

class UsdToCurrencyAPIView(GenericAPIView):
    serializer_class = ExchangeRateResponseSerializer
    permission_classes = [AllowAny]

    def get(self, request, currency: str):
        service = ExchangeRateService()

        try:
            rate = service.get_usd_to_currency(currency.upper())
        except RuntimeError as e:
            raise ValidationError({"currency": str(e)})
        
        data = {
            "base": "USD",
            "target": currency.upper(),
            "rate": rate,
        }
    
        serializer = self.get_serializer(instance=data)
        return Response(serializer.data)
    
class ExchangeHistoryAPIView(GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def get(self, request):
        repo = DjangoAccountRepository()
        account = repo.find_by_user_id(request.user.id)
        if not account:
            return Response({"error": "Account not found"}, status=404)
        
        currency = request.query_params.get("currency", account.country.currency).upper()
        period = request.query_params.get("period", "6m")

        period_map = {
            "3m": 3,
            "6m": 6,
            "1y": 12,
            "2y": 24,
        }

        if period not in period_map:
            return Response({
                "error": "period must be one of: 3m, 6m, 1y, 2y"
            }, status=400)
        
        months = period_map[period]
        history = ExchangeHistoryService().get_usd_history_until_today(
            currency=currency,
            months=months,
        )
        
        return Response({
            "base": "USD",
            "target": currency,
            "period": period,
            "end_date": str(__import__("datetime").date.today()),
            "history": history
        })
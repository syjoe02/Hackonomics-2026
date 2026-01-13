from django.urls import path
from exchange.presentation.views import UsdToCurrencyAPIView, ExchangeHistoryAPIView

urlpatterns = [
    path("usd-to/<str:currency>/", UsdToCurrencyAPIView.as_view(), name="usd-to-currency"),
    path("history/", ExchangeHistoryAPIView.as_view(), name="exchange-history"),
]
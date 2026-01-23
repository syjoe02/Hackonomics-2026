from django.urls import path

from accounts.presentation.views import AccountView, MyExchangeRateAPIView

urlpatterns = [
    path("me/", AccountView.as_view()),
    path("me/exchange-rate/", MyExchangeRateAPIView.as_view()),
]

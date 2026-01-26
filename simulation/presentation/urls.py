from django.urls import path
from simulation.presentation.views import CompareDcaVsDepositAPIView

urlpatterns = [
    path(
        "compare/dca-vs-deposit/",
        CompareDcaVsDepositAPIView.as_view(),
        name="compare-dca-vs-deposit",
    ),
]
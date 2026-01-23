from django.urls import path

from .views import CountryDetailAPIView, CountryListAPIView

urlpatterns = [
    path("countries/", CountryListAPIView.as_view(), name="country-list"),
    path(
        "countries/<str:code>/", CountryDetailAPIView.as_view(), name="country-detail"
    ),
]

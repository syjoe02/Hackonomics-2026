from django.urls import path

from .views import BusinessNewsRefreshView, BusinessNewsView

urlpatterns = [
    path("business-news/", BusinessNewsView.as_view(), name="business-news"),
    path(
        "business-news/refresh/",
        BusinessNewsRefreshView.as_view(),
        name="business-news-refresh",
    ),
]

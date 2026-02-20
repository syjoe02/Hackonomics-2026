from django.urls import path

from .views import BusinessNewsView

urlpatterns = [
    path("business-news/", BusinessNewsView.as_view(), name="business-news"),
]

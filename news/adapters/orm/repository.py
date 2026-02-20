from datetime import timedelta

from django.utils import timezone

from news.adapters.orm.models import BusinessNewsModel
from news.application.ports.business_news_repository import BusinessNewsRepository
from news.domain.entities import BusinessNews


class DjangoBusinessNewsRepository(BusinessNewsRepository):

    def find_recent_by_country(self, country_code: str):
        three_days_ago = timezone.now() - timedelta(days=3)

        row = (
            BusinessNewsModel.objects.filter(
                country_code=country_code, created_at__gte=three_days_ago
            )
            .order_by("-created_at")
            .first()
        )

        if not row:
            return None

        return BusinessNews(
            country_code=row.country_code,
            content=row.content,
            created_at=row.created_at,
        )

    def save(self, news: BusinessNews) -> None:
        BusinessNewsModel.objects.create(
            country_code=news.country_code,
            content=news.content,
        )

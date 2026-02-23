from django.utils import timezone

from news.adapters.orm.models import BusinessNewsModel
from news.application.ports.business_news_repository import BusinessNewsRepository
from news.domain.entities import BusinessNews


class DjangoBusinessNewsRepository(BusinessNewsRepository):

    def find_latest(self, country_code: str) -> BusinessNews | None:
        obj = (
            BusinessNewsModel.objects
            .filter(country_code=country_code)
            .order_by("-created_at")
            .first()
        )

        if not obj:
            return None

        return Business_news_from_model(obj)

    def is_recent(self, country_code: str, minutes: int = 180) -> bool:
        latest = (
            BusinessNewsModel.objects
            .filter(country_code=country_code)
            .order_by("-created_at")
            .only("created_at")
            .first()
        )

        if not latest:
            return False

        return (timezone.now() - latest.created_at).total_seconds() < minutes * 60

    def save(self, news: BusinessNews) -> None:
        latest = self.find_latest(news.country_code)

        if latest and latest.content == news.content:
            return  # skip duplicate content

        BusinessNewsModel.objects.create(
            country_code=news.country_code,
            content=news.content,
            created_at=news.created_at,
        )


def Business_news_from_model(obj: BusinessNewsModel) -> BusinessNews:
    return BusinessNews(
        country_code=obj.country_code,
        content=obj.content,
        created_at=obj.created_at,
    )
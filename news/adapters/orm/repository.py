from news.adapters.orm.models import BusinessNewsModel
from news.application.ports.business_news_repository import BusinessNewsRepository
from news.domain.entities import BusinessNews


class DjangoBusinessNewsRepository(BusinessNewsRepository):

    def find_recent_by_country(self, country_code: str):
        obj = (
            BusinessNewsModel.objects.filter(country_code=country_code)
            .order_by("-created_at")
            .first()
        )

        if not obj:
            return None

        return BusinessNews(
            country_code=obj.country_code,
            content=obj.content,
            created_at=obj.created_at,
        )

    def save(self, news: BusinessNews) -> None:
        BusinessNewsModel.objects.create(
            country_code=news.country_code,
            content=news.content,
            created_at=news.created_at,
        )

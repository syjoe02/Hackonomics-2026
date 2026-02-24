from news.adapters.orm.models import BusinessNewsModel
from news.application.ports.business_news_repository import BusinessNewsRepository
from news.domain.entities import BusinessNews


class DjangoBusinessNewsRepository(BusinessNewsRepository):

    def find_latest(self, country_code: str) -> BusinessNews | None:
        obj = (
            BusinessNewsModel.objects.filter(country_code=country_code)
            .order_by("-created_at")
            .first()
        )

        if not obj:
            return None

        return self._to_entity(obj)

    def save(self, news: BusinessNews) -> None:
        latest = self.find_latest(news.country_code)

        if latest and latest.content == news.content:
            return

        BusinessNewsModel.objects.create(
            country_code=news.country_code,
            content=news.content,
            created_at=news.created_at,
        )

    @staticmethod
    def _to_entity(obj: BusinessNewsModel) -> BusinessNews:
        return BusinessNews(
            country_code=obj.country_code,
            content=obj.content,
            created_at=obj.created_at,
        )

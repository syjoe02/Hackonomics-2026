from django.utils import timezone

from accounts.application.ports.repository import AccountRepository
from news.application.ports.business_news_port import BusinessNewsPort
from news.application.ports.business_news_repository import BusinessNewsRepository
from news.domain.entities import BusinessNews
from user_calendar.domain.value_objects import UserId


class BusinessNewsService:

    def __init__(
        self,
        account_repo: AccountRepository,
        news_port: BusinessNewsPort,
        news_repo: BusinessNewsRepository,
    ):
        self.account_repo = account_repo
        self.news_port = news_port
        self.news_repo = news_repo

    def get_user_business_news(self, user_id: UserId):
        account = self.account_repo.find_by_user_id(user_id.value)
        if not account or not account.country:
            return "Country not set."

        country_code = account.country.code

        cached = self.news_repo.find_recent_by_country(country_code)
        if cached:
            return cached.content

        try:
            news_text = self.news_port.get_country_news(country_code)
        except Exception:
            news_text = "Business news temporarily unavailable."

        if not news_text.strip():
            news_text = "No major business news in the last 3 days."

        self.news_repo.save(
            BusinessNews(
                country_code=country_code,
                content=news_text,
                created_at=timezone.now(),
            )
        )

        return news_text

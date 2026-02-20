from django.utils import timezone

from accounts.application.ports.repository import AccountRepository
from common.ai.json_cleaner import clean_json_response
from common.ai.response_validator import validate_news_items
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
            return []

        country_code = account.country.code

        news_items = []  # ✅ ALWAYS initialize

        try:
            raw_text = self.news_port.get_country_news(country_code)

            print("=== GEMINI RAW OUTPUT ===", flush=True)
            print(raw_text, flush=True)

            cleaned = clean_json_response(raw_text)
            validated = validate_news_items(cleaned)

            news_items = validated

        except Exception as e:
            print("=== GEMINI ERROR ===", flush=True)
            print(str(e), flush=True)

        # fallback if AI failed
        if not news_items:
            news_items = [
                {
                    "title": "News unavailable",
                    "description": "Unable to retrieve business news at this time.",
                }
            ]

        self.news_repo.save(
            BusinessNews(
                country_code=country_code,
                content=news_items,
                created_at=timezone.now(),
            )
        )

        return news_items

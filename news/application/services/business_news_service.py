from django.core.cache import cache
from django.utils import timezone
import logging

from accounts.application.ports.repository import AccountRepository
from common.ai.json_cleaner import clean_json_response
from common.ai.response_validator import validate_news_items
from news.application.ports.business_news_port import BusinessNewsPort
from news.application.ports.business_news_repository import BusinessNewsRepository
from news.domain.entities import BusinessNews
from user_calendar.domain.value_objects import UserId

logger = logging.getLogger(__name__)

CACHE_TTL = 60 * 60 * 6


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
        cache_key = f"business_news:{country_code}"

        cached = cache.get(cache_key)
        if cached:
            return cached

        latest = self.news_repo.find_latest(country_code)
        if latest:
            cache.set(cache_key, latest.content, CACHE_TTL)
            return latest.content

        return [
            {
                "title": "News unavailable",
                "description": "Unable to retrieve business news at this time.",
            }
        ]
    
    def fetch_and_store_news(self, country_code: str):
        try:
            validated = self.news_port.get_country_news(country_code)

            if not validated:
                logger.warning(f"No valid news returned for {country_code}")
                return

            news = BusinessNews(
                country_code=country_code,
                content=validated,
                created_at=timezone.now(),
            )

            self.news_repo.save(news)

            cache_key = f"business_news:{country_code}"
            cache.set(cache_key, validated, CACHE_TTL)

            logger.info(f"News updated for {country_code}")

        except Exception as e:
            logger.exception(f"Gemini fetch failed for {country_code}: {str(e)}")
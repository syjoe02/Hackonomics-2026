from celery import shared_task
from django.utils import timezone
import logging

from news.application.services.business_news_service import BusinessNewsService
from news.adapters.orm.repository import DjangoBusinessNewsRepository
from news.adapters.gemini.business_news_adapter import GeminiBusinessNewsAdapter
from accounts.adapters.orm.repository import DjangoAccountRepository

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=60,      # retry after 60s, then exponential
    retry_backoff_max=600, # max 10 minutes
    retry_kwargs={"max_retries": 3},
)


def fetch_business_news(self):

    logger.info("Starting business news fetch task")

    service = BusinessNewsService(
        account_repo=DjangoAccountRepository(),
        news_port=GeminiBusinessNewsAdapter(),
        news_repo=DjangoBusinessNewsRepository(),
    )

    countries = service.account_repo.get_all_country_codes()

    if not countries:
        logger.info("No countries found — skipping fetch")
        return

    now = timezone.now()

    for code in countries:
        try:
            # Prevent duplicate
            latest = service.news_repo.find_latest(code)

            if latest and (now - latest.created_at).total_seconds() < 3 * 3600:
                logger.info(f"Skipping {code}: recently updated")
                continue

            logger.info(f"Fetching news for {code}")

            service.fetch_and_store_news(code)

        except Exception as e:
            logger.exception(f"Failed fetching news for {code}: {str(e)}")

    logger.info("Business news fetch completed")
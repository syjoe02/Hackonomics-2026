import logging
from typing import Optional

from celery import shared_task

from accounts.adapters.orm.repository import DjangoAccountRepository
from news.adapters.gemini.business_news_adapter import GeminiBusinessNewsAdapter
from news.adapters.orm.repository import DjangoBusinessNewsRepository
from news.application.services.business_news_service import BusinessNewsService

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=60,  # retry after 60s, then exponential
    retry_backoff_max=600,  # max 10 minutes
    retry_kwargs={"max_retries": 3},
)
def fetch_business_news(self, country_code: Optional[str] = None) -> None:
    service = BusinessNewsService(
        account_repo=DjangoAccountRepository(),
        news_port=GeminiBusinessNewsAdapter(),
        news_repo=DjangoBusinessNewsRepository(),
    )
    task_id = getattr(self.request, "id", None)

    if country_code:
        logger.info("[task:%s] manual refresh → %s", task_id, country_code)
        service.fetch_and_store_news(country_code)
        logger.info("[task:%s] manual refresh done → %s", task_id, country_code)
        return

    countries = service.account_repo.get_all_country_codes()
    if not countries:
        logger.info("[task:%s] no countries found — skipping", task_id)
        return

    logger.info(
        "[task:%s] scheduled refresh start — %d countries", task_id, len(countries)
    )

    for code in countries:
        try:
            service.fetch_and_store_news(code)
        except Exception:
            logger.exception("[task:%s] failed refreshing %s", task_id, code)

    logger.info("[task:%s] scheduled refresh completed", task_id)

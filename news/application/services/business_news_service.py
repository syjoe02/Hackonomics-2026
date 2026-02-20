from accounts.application.ports.repository import AccountRepository
from common.errors.error_codes import ErrorCode
from common.errors.exceptions import BusinessException
from news.application.ports.business_news_port import BusinessNewsPort
from user_calendar.domain.value_objects import UserId


class BusinessNewsService:
    def __init__(
        self,
        account_repo: AccountRepository,
        news_port: BusinessNewsPort,
    ):
        self.account_repo = account_repo
        self.news_port = news_port

    def get_user_business_news(self, user_id: UserId) -> str:
        account = self.account_repo.find_by_user_id(user_id.value)

        if not account:
            raise BusinessException(ErrorCode.DATA_NOT_FOUND)

        if not account.country:
            raise BusinessException(ErrorCode.DATA_NOT_FOUND)

        country_code = account.country.code

        return self.news_port.get_country_news(country_code)

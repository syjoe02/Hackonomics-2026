from typing import Dict

from accounts.application.ports.repository import AccountRepository
from common.errors.error_codes import ErrorCode
from common.errors.exceptions import BusinessException


class GetAccountUseCase:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def execute(self, user_id: int) -> Dict[str, str]:
        account = self.repository.find_by_user_id(user_id)

        if not account:
            raise BusinessException(ErrorCode.DATA_NOT_FOUND)
        if account.country is None or account.income is None:
            raise BusinessException(ErrorCode.DATA_NOT_FOUND)

        return {
            "country_code": account.country.code,
            "currency": account.country.currency,
            "annual_income": str(account.income.amount),
            "monthly_investable_amount": str(account.monthly_investable_amount),
        }

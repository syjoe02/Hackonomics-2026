from accounts.application.dto import AccountUpdateCommand
from accounts.application.ports.repository import AccountRepository
from accounts.application.ports.event_publisher import DomainEventPublisher
from accounts.domain.entities import Account
from accounts.domain.value_objects import Country, AnnualIncome

from common.errors.exceptions import BusinessException
from common.errors.error_codes import ErrorCode

class GetAccountUseCase:
    def __init__(self, repository: AccountRepository, event_publisher: DomainEventPublisher):
        self.repository = repository
        self.event_publisher = event_publisher

    def execute(self, user_id: int, command: AccountUpdateCommand) -> None:
        account = self.repository.find_by_user_id(user_id)

        country = Country(
            code=command.country_code,
            currency=command.currency,
        )
        income = AnnualIncome(command.annual_income)
        
        if account is None:
            account = Account(
                user_id=user_id,
                country=country,
                income=income,
                monthly_investable_amount=command.monthly_investable_amount,
            )
        else:
            account.update_country(country)
            account.update_income(income)
            account.update_monthly_investable_amount(command.monthly_investable_amount)

        self.repository.save(account)

        self.event_publisher.publish(
            event_type="ACCOUNT_UPDATED",
            payload={"user_id": user_id},
        )

class UpdateAccountUseCase:
    def __init__(self, repository: AccountRepository, event_publisher: DomainEventPublisher):
        self.repository = repository
        self.event_publisher = event_publisher

    def execute(self, user_id: int, command: AccountUpdateCommand) -> None:
        account = self.repository.find_by_user_id(user_id)

        country = Country(
            code=command.country_code,
            currency=command.currency,
        )
        income = AnnualIncome(command.annual_income)

        if account is None:
            account = Account(
                user_id=user_id,
                country=country,
                income=income,
                monthly_investable_amount = command.monthly_investable_amount,
            )
        else:
            account.update_country(country)
            account.update_income(income)
            account.update_monthly_investable_amount(command.monthly_investable_amount)
        
        self.repository.save(account)

        self.event_publisher.publish(
            event_type="ACCOUNT_UPDATED",
            payload={"user_id": user_id},
        )

class GetExchangeRateUseCase:
    def __init__(self, repository: AccountRepository, exchange_service):
        self.repository = repository
        self.exchange_service = exchange_service

        def execute(self, user_id: int) -> dict:
            account = self.repository.find_by_user_id(user_id)
            if not account:
                raise BusinessException(ErrorCode.DATA_NOT_FOUND)
            
            currency = account.country.currency.upper()
            rate = self.exchange_service.get_usd_to_currency(currency)

            return {
                "base": "USD",
                "target": currency,
                "rate": rate,
            }
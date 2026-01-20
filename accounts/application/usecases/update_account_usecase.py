from accounts.application.dto import AccountUpdateCommand
from accounts.application.ports.repository import AccountRepository
from accounts.application.ports.event_publisher import DomainEventPublisher
from accounts.domain.entities import Account
from accounts.domain.value_objects import Country, AnnualIncome
from common.errors.exceptions import BusinessException
from common.errors.handlers import ErrorCode

class UpdateAccountUseCase:
    def __init__(
        self,
        repository: AccountRepository,
        event_publisher: DomainEventPublisher,
    ):
        self.repository = repository
        self.event_publisher = event_publisher

    def execute(self, user_id: int, command: AccountUpdateCommand) -> None:
        if not user_id:
            raise BusinessException(ErrorCode.UNAUTHORIZED)
        # Create new Account
        if account is None:
            account = Account(
                user_id=user_id,
                country=None,
                income=None,
                monthly_investable_amount=None,
            )
            self.repository.save(account)

            self.event_publisher.publish(
                event_type="ACCOUNT_CREATED",
                payload={"user_id": user_id},
            )
            return
        # Edit 
        if command.country_code and command.currency:
            country = Country(
                code=command.country_code,
                currency=command.currency,
            )
            account.update_country(country)

        if command.annual_income is not None:
            income = AnnualIncome(command.annual_income)
            account.update_income(income)

        if command.monthly_investable_amount is not None:
            account.update_monthly_investable_amount(command.monthly_investable_amount)
            
            self.repository.save(account)
            self.event_publisher.publish(
                event_type="ACCOUNT_CREATED",
                payload={"user_id": user_id},
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
from accounts.application.dto import AccountUpdateCommand
from accounts.application.ports.repository import AccountRepository
from accounts.application.ports.event_publisher import DomainEventPublisher
from accounts.domain.entities import Account
from accounts.domain.value_objects import Country, AnnualIncome

class UpdateAccountUseCase:
    def __init__(
        self,
        repository: AccountRepository,
        event_publisher: DomainEventPublisher,
    ):
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
            account.update_monthly_investable_amount(
                command.monthly_investable_amount
            )

        self.repository.save(account)

        self.event_publisher.publish(
            event_type="ACCOUNT_UPDATED",
            payload={"user_id": user_id},
        )
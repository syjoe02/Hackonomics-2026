from accounts.application.ports.repository import AccountRepository
from accounts.domain.entities import Account
from accounts.domain.value_objects import Country, AnnualIncome
from accounts.adapters.orm.models import AccountModel

class DjangoAccountRepository(AccountRepository):
    def find_by_user_id(self, user_id: int):
        try:
            m = AccountModel.objects.get(user_id=user_id)
        except AccountModel.DoesNotExist:
            return None

        return Account(
            user_id=m.user_id,
            country=Country(m.country_code, m.currency),
            income=AnnualIncome(m.annual_income),
            monthly_investable_amount=m.monthly_investable_amount,
        )

    def save(self, account: Account) -> None:
        AccountModel.objects.update_or_create(
            user_id=account.user_id,
            defaults={
                "country_code": account.country.code,
                "currency": account.country.currency,
                "annual_income": account.income.amount,
                "monthly_investable_amount": account.monthly_investable_amount,
            },
        )
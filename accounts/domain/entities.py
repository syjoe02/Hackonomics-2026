from dataclasses import dataclass, field
from decimal import Decimal

from accounts.domain.value_objects import Country, AnnualIncome

@dataclass
class Account:
    user_id : int
    country : Country
    income : AnnualIncome
    monthly_investable_amount : Decimal

    def update_country(self, country: Country):
        self.country = country

    def update_income(self, income: AnnualIncome):
        self.income = income
    
    def update_monthly_investable_amount(self, amount: Decimal):
        self.monthly_investable_amount = amount
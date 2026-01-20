from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from accounts.domain.value_objects import Country, AnnualIncome

@dataclass
class Account:
    # Django User model "id" == user_id
    user_id : int
    country : Optional[Country]
    income : Optional[AnnualIncome]
    monthly_investable_amount : Optional[Decimal]

    def update_country(self, country: Country):
        self.country = country

    def update_income(self, income: AnnualIncome):
        self.income = income
    
    def update_monthly_investable_amount(self, amount: Decimal):
        self.monthly_investable_amount = amount
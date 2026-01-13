from dataclasses import dataclass, field
from typing import List
from accounts.domain.value_objects import Country, AnnualIncome

@dataclass
class Account:
    user_id : int
    country : Country
    income : AnnualIncome
    monlty_investable_amount : int

    def update_country(self, country: Country):
        self.country = country

    def update_income(self, income: AnnualIncome):
        self.income = income
    
    def update_monlty_investable_amount(self, amount: int):
        self.monlty_investable_amount = amount
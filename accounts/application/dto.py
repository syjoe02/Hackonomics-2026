from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class AccountUpdateCommand:
    country_code: str
    currency: str
    annual_income: int
    monthly_investable_amount: int
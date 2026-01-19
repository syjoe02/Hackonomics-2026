from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class AccountUpdateCommand:
    country_code: str
    currency: str
    annual_income: Decimal
    monthly_investable_amount: Decimal
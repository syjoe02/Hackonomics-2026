from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass(frozen=True)
class AccountUpdateCommand:
    country_code: Optional[str]
    currency: Optional[str]
    annual_income: Optional[Decimal]
    monthly_investable_amount: Optional[Decimal]
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Country:
    code: str
    currency: str

@dataclass(frozen=True)
class AnnualIncome:
    amount: Decimal

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError("Annual income must be positive")
    
    @property
    def monthly_amount(self) -> int:
        return self.amount // 12
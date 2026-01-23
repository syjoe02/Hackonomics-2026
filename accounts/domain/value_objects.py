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
        if self.amount is None:
            raise ValueError("AnnualIncome cannot be None")

        if self.amount <= 0:
            raise ValueError("AnnualIncome must be greater than 0")

        object.__setattr__(self, "amount", Decimal(self.amount))

    @property
    def monthly(self) -> Decimal:
        return self.amount / Decimal("12")
from datetime import datetime
from typing import List, Dict
from decimal import Decimal, getcontext

from simulation.domain.entities import SimulationResult
from accounts.application.ports.repository import AccountRepository
from exchange.application.services import ExchangeHistoryService
from common.errors.exceptions import BusinessException
from common.errors.error_codes import ErrorCode

getcontext().prec = 28

class CompareInvestmentUseCase:
    PERIOD_MAP = {
        "1y": 12,
        "2y": 24,
    }

    def __init__(
        self,
        account_repository: AccountRepository,
        exchange_history_service: ExchangeHistoryService,
    ):
        self.account_repository = account_repository
        self.exchange_history_service = exchange_history_service

    def execute(
        self,
        user_id: int,
        period: str,
        deposit_rate: float,
    ) -> dict:
    
        if period not in self.PERIOD_MAP:
            raise BusinessException(ErrorCode.INVALID_PARAMETER)

        if deposit_rate < 0:
            raise BusinessException(ErrorCode.INVALID_PARAMETER)
        deposit_rate = Decimal(str(deposit_rate))

        account = self.account_repository.find_by_user_id(user_id)
        if not account:
            raise BusinessException(ErrorCode.DATA_NOT_FOUND)

        monthly_amount = Decimal(str(account.monthly_investable_amount))
        if monthly_amount <= 0:
            raise BusinessException(ErrorCode.INVALID_PARAMETER)
        
        currency = account.country.currency.upper()

        history = self.exchange_history_service.get_usd_history_until_today(
            currency=currency,
            period=period,
        )
        if not history:
            raise BusinessException(ErrorCode.DATA_NOT_FOUND)

        months = self.PERIOD_MAP[period]
        monthly_rates = self._extract_monthly_rates(history, months)
        if len(monthly_rates) < months:
            raise BusinessException(ErrorCode.DATA_NOT_FOUND)            

        # USD, DCA simulation start
        total_usd = Decimal("0")
        total_invested = Decimal("0")

        for h in monthly_rates:
            rate = Decimal(str(h["rate"])) # 1 USD = rate target currency
            usd = monthly_amount / rate
            total_usd += usd
            total_invested += monthly_amount

        last_rate = Decimal(str(history[-1]["rate"]))
        usd_final = total_usd * last_rate
        # Fixed deposit
        deposit_final = total_invested * (Decimal("1") + deposit_rate / Decimal("100"))

        if usd_final > deposit_final:
            winner = "usd"
            diff = (usd_final - deposit_final) / deposit_final * 100
        else:
            winner = "deposit"
            diff = (deposit_final - usd_final) / usd_final * 100

        return SimulationResult(
            currency=currency,
            period=period,
            monthly_amount=monthly_amount,
            deposit_rate=deposit_rate,
            total_invested=total_invested,
            usd_final=usd_final,
            deposit_final=deposit_final,
            winner=winner,
            diff_percent=diff,
            summary=self._make_summary(winner, diff, currency),
        )

    def _extract_monthly_rates(
            self,
            history: List[Dict],
            months: int,
        ) -> List[Dict]:

            monthly = []
            seen = set()

            for h in history:
                d = datetime.fromisoformat(h["date"])
                key = (d.year, d.month)

                if key not in seen:
                    monthly.append(h)
                    seen.add(key)

                if len(monthly) == months:
                    break

            return monthly

    def _make_summary(self, winner: str, diff: Decimal, currency: str) -> str:
        diff = round(diff, 2)

        if winner == "usd":
            return (
                f"Over this period, investing in USD through Dollar-Cost Averaging (DCA) "
                f"outperformed the fixed-term deposit by approximately {diff}%. "
                f"({currency} based)"
            )
        else:
            return (
                f"Over this period, the fixed-term deposit outperformed investing in USD "
                f"through Dollar-Cost Averaging (DCA) by approximately {diff}%. "
                f"({currency} based)"
            )
from datetime import date
from typing import List, TypedDict

import requests
from dateutil.relativedelta import relativedelta

from common.errors.error_codes import ErrorCode
from common.errors.exceptions import BusinessException
from exchange.infra.exchange_rate_client import ExchangeRateClient
from exchange.infra.frankfurter_client import FrankfurterClient


class ExchangeRateService:
    # default = 1 USD
    def __init__(self) -> None:
        self.client = ExchangeRateClient()

    def get_usd_to_currency(self, currency: str) -> float:
        try:
            return self.client.get_rate(
                target_currency=currency,
                base="USD",
            )
        except ValueError:
            raise BusinessException(ErrorCode.INVALID_PARAMETER)


class _HistoryRow(TypedDict):
    date: str
    rate: float


class ExchangeHistoryService:
    PERIOD_MAP = {
        "3m": 3,
        "6m": 6,
        "1y": 12,
        "2y": 24,
    }
    DEFAULT_CURRENCY = "CAD"
    DEFAULT_PERIOD = "6m"

    def __init__(self) -> None:
        self.client = FrankfurterClient()

    def get_usd_history_until_today(
        self, currency: str, period: str
    ) -> List[_HistoryRow]:
        currency = (currency or self.DEFAULT_CURRENCY).upper()
        period = period or self.DEFAULT_PERIOD

        if period not in self.PERIOD_MAP:
            raise BusinessException(ErrorCode.INVALID_PARAMETER)

        months = self.PERIOD_MAP[period]
        end = date.today()
        start = end - relativedelta(months=months)

        try:
            raw = self.client.get_historical(
                start=start.isoformat(),
                end=end.isoformat(),
                base="USD",
                target=currency,
            )
        except requests.exceptions.Timeout:
            raise BusinessException(ErrorCode.TIMEOUT)
        except requests.exceptions.RequestException:
            raise BusinessException(ErrorCode.EXTERNAL_API_FAILED)

        rates = raw.get("rates")
        if not rates:
            raise BusinessException(ErrorCode.DATA_NOT_FOUND)

        history: List[_HistoryRow] = []
        for d in sorted(rates.keys()):
            day_rates = rates[d]

            if currency not in day_rates:
                raise BusinessException(ErrorCode.INVALID_RESPONSE)

            history.append(
                {
                    "date": d,
                    "rate": rates[d][currency],
                }
            )

        return history

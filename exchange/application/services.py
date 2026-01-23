from datetime import date

from dateutil.relativedelta import relativedelta

from common.errors.error_codes import ErrorCode
from common.errors.exceptions import BusinessException
from exchange.infra.exchange_rate_client import ExchangeRateClient
from exchange.infra.frankfurter_client import FrankfurterClient


class ExchangeRateService:
    # default = 1 USD
    def __init__(self):
        self.client = ExchangeRateClient()

    def get_usd_to_currency(self, currency: str) -> float:
        try:
            return self.client.get_rate(
                target_currency=currency,
                base="USD",
            )
        except ValueError as e:
            raise BusinessException(ErrorCode.INVALID_PARAMETER, str(e))


class ExchangeHistoryService:
    PERIOD_MAP = {
        "3m": 3,
        "6m": 6,
        "1y": 12,
        "2y": 24,
    }

    def __init__(self):
        self.client = FrankfurterClient()

    def get_usd_history_until_today(self, currency: str, period: int):
        if not currency:
            raise BusinessException(ErrorCode.INVALID_PARAMETER)

        if period not in self.PERIOD_MAP:
            raise BusinessException(ErrorCode.INVALID_PARAMETER)

        months = self.PERIOD_MAP[period]
        end = date.today()
        start = end - relativedelta(months=months)

        raw = self.client.get_historical(
            start=start.isoformat(),
            end=end.isoformat(),
            base="USD",
            target=currency,
        )
        rates = raw.get("rates")
        if not rates:
            raise BusinessException(ErrorCode.DATA_NOT_FOUND)

        history = []
        for d in sorted(rates.keys()):
            history.append(
                {
                    "date": d,
                    "rate": rates[d][currency],
                }
            )

            return history

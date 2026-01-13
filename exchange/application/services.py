from exchange.infra.exchange_rate_client import ExchangeRateClient
from exchange.infra.frankfurter_client import FrankfurterClient

from datetime import date
from dateutil.relativedelta import relativedelta

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
            raise RuntimeError(str(e))
    
class ExchangeHistoryService:
    def __init__(self):
        self.client = FrankfurterClient()
    
    def get_usd_history_until_today(self, currency: str, months: int):
        end = date.today()
        start = end - relativedelta(months=months)

        raw = self.client.get_historical(
            start=start.isoformat(),
            end=end.isoformat(),
            base="USD",
            target=currency,
        )
        history = []
        rates = raw["rates"]

        for d in sorted(rates.keys()):
            history.append({
                "date": d, 
                "rate": rates[currency],
            })

            return history

import requests
import os

class ExchangeRateClient:
    BASE_URL = "https://api.frankfurter.app"

    def get_rate(self, target_currency: str, base: str = "USD") -> float:
        url = f"{self.BASE_URL}/latest"

        params = {
            "from": base,
            "to": target_currency
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 404:
            raise ValueError(f"Currency {target_currency} is not suppoerted by Frankfurter API")

        response.raise_for_status()
        data = response.json()
        
        try:
            return data["rates"][target_currency]
        except KeyError:
            raise ValueError(f"Currency {target_currency} not found in response")


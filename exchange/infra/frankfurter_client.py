import requests

class FrankfurterClient:
    BASE_URL = "https://api.frankfurter.app"

    def get_historical(self, start: str, end: str, base: str, target: str):
        url = f"{self.BASE_URL}/{start}..{end}"
        params = {
            "from": base,
            "to": target,
        }

        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
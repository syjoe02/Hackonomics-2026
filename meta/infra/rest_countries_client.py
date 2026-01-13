import requests

BASE_URL = "https://restcountries.com/v3.1"

class RestCountriesClient:
    def fetch_all(self):
        url = f"{BASE_URL}/all?fields=cca2,name,currencies,flags"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def fetch_by_code(self, code: str):
        url = f"{BASE_URL}/alpha/{code}?fields=cca2,name,currencies,flags"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
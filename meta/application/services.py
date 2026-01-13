from meta.infra.rest_countries_client import RestCountriesClient

class CountryService:
    def __init__(self):
        self.client = RestCountriesClient()
    
    def get_all_countries(self):
        raw = self.client.fetch_all()
        print(raw)
        result = []
        for item in raw:
            try:
                result.append(self._map_country(item))
            except Exception:
                continue
        return result
    
    def get_country(self, country_code: str):
        raw = self.client.fetch_by_code(country_code)

        if isinstance(raw, dict):
            item = raw
        elif isinstance(raw, list) and len(raw) > 0:
            item = raw[0]
        else:
            raise ValueError("Invalid country response")
        
        return self._map_country(item)
    
    def _is_valid(self, item):
        return "cca2" in item and "currencies" in item and item["currencies"]
    
    def _map_country(self, item):
        code = item["cca2"]
        name = item["name"]["common"]
        currencies = item.get("currencies", {})
        if not currencies:
            raise ValueError("No Currency")
        
        currency_codes = list(currencies.keys())
        default_currency = currency_codes[0]

        flag = item.get("flags", {}).get("png")

        return {
            "code": code,
            "name": name,
            "currencies": currency_codes,
            "default_currency": default_currency,
            "flag": flag,
        }
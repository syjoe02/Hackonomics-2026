from common.errors.error_codes import ErrorCode
from common.errors.exceptions import BusinessException
from meta.infra.rest_countries_client import RestCountriesClient


class CountryService:
    def __init__(self):
        self.client = RestCountriesClient()

    def get_all_countries(self):
        try:
            raw = self.client.fetch_all()
        except Exception:
            raise BusinessException(ErrorCode.EXTERNAL_API_FAILED)

        result = []
        for item in raw:
            try:
                result.append(self._map_country(item))
            except Exception:
                continue

        if not result:
            raise BusinessException(ErrorCode.DATA_NOT_FOUND)

        return result

    def get_country(self, country_code: str):
        try:
            raw = self.client.fetch_by_code(country_code)
        except Exception:
            raise BusinessException(ErrorCode.EXTERNAL_API_FAILED)

        if isinstance(raw, dict):
            item = raw
        elif isinstance(raw, list) and len(raw) > 0:
            item = raw[0]
        else:
            raise BusinessException(ErrorCode.DATA_NOT_FOUND)

        try:
            return self._map_country(item)
        except Exception:
            raise BusinessException(ErrorCode.INVALID_RESPONSE)

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

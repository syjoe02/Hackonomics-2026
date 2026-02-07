from decimal import ROUND_DOWN, Decimal
from typing import Any, Dict

from rest_framework import serializers

from meta.application.services import CountryService


class AccountUpdateSerializer(serializers.Serializer):
    country_code = serializers.CharField(max_length=2)
    currency = serializers.CharField(max_length=3)
    annual_income = serializers.DecimalField(max_digits=15, decimal_places=2)
    monthly_investable_amount = serializers.DecimalField(
        max_digits=15, decimal_places=2, min_value=Decimal("0")
    )

    def _get_country_or_raise(self, country_code: str) -> Dict[str, Any]:
        try:
            return CountryService().get_country(country_code)
        except Exception:
            raise serializers.ValidationError(
                {"country_code": f"Invalid country code: {country_code}"}
            )

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        country_code = attrs["country_code"].upper()
        currency = attrs["currency"].upper()
        # Decimal type
        annual_income: Decimal = Decimal(attrs["annual_income"])
        monthly_amount: Decimal = Decimal(attrs["monthly_investable_amount"])
        # Fix to 2 decimal places
        annual_income = annual_income.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
        monthly_amount = monthly_amount.quantize(Decimal("0.01"), rounding=ROUND_DOWN)

        country = self._get_country_or_raise(country_code)
        valid_currencies = [c.upper() for c in country.get("currencies", [])]

        if currency not in valid_currencies:
            raise serializers.ValidationError(
                {"currency": (f"{currency} is not valid for country {country_code}")}
            )

        attrs.update(
            {
                "country_code": country_code,
                "currency": currency,
                "annual_income": annual_income,
                "monthly_investable_amount": monthly_amount,
            }
        )
        return attrs

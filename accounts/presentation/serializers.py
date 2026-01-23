from decimal import ROUND_DOWN, Decimal

from rest_framework import serializers

from meta.application.services import CountryService


class AccountUpdateSerializer(serializers.Serializer):
    country_code = serializers.CharField(max_length=2)
    currency = serializers.CharField(max_length=3)
    annual_income = serializers.DecimalField(max_digits=15, decimal_places=2)
    monthly_investable_amount = serializers.DecimalField(
        max_digits=15, decimal_places=2, min_value=Decimal("0")
    )

    def validate(self, attrs):
        country_code = attrs["country_code"].upper()
        currency = attrs["currency"].upper()
        # Decimal type
        annual_income: Decimal = Decimal(attrs["annual_income"])
        monthly_amount: Decimal = Decimal(attrs["monthly_investable_amount"])
        # Fix to 2 decimal places
        annual_income = annual_income.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
        monthly_amount = monthly_amount.quantize(Decimal("0.01"), rounding=ROUND_DOWN)

        try:
            country = CountryService().get_country(country_code)
        except Exception:
            raise serializers.ValidationError(
                {"country_code": f"Invalid country code: {country_code}"}
            )
        valid_currencies = [c.upper() for c in country["currencies"]]

        if currency not in valid_currencies:
            raise serializers.ValidationError(
                {"currency": f"{currency} is not valid for country {country_code}"}
            )

        attrs["country_code"] = country_code
        attrs["currency"] = currency
        attrs["annual_income"] = annual_income
        attrs["monthly_investable_amount"] = monthly_amount
        return attrs

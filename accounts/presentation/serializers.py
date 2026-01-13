from rest_framework import serializers
from meta.application.services import CountryService

class AccountUpdateSerializer(serializers.Serializer):
    country_code = serializers.CharField()
    currency = serializers.CharField()
    annual_income = serializers.IntegerField()
    monthly_investable_amount = serializers.IntegerField(min_value=0)

    def validate(self, attrs):
        country_code = attrs["country_code"]
        currency = attrs["currency"]
        country = CountryService().get_country(country_code)
        valid_currencies = country["currencies"]

        if currency not in valid_currencies:
            raise serializers.ValidationError({
                "currency": f"{currency} is not valid for country {country_code}"
            })
        
        return attrs
from rest_framework import serializers

class CountrySerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    currencies = serializers.ListField(
        child=serializers.CharField()
    )
    default_currency = serializers.CharField()
    flag = serializers.URLField(required=False, allow_null=True)
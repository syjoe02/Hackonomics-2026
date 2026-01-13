from rest_framework import serializers

class ExchangeRateResponseSerializer(serializers.Serializer):
    base = serializers.CharField()
    target = serializers.CharField()
    rate = serializers.FloatField()

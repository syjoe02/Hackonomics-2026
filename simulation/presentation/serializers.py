from rest_framework import serializers


class CompareSimulationRequestSerializer(serializers.Serializer):
    period = serializers.ChoiceField(choices=["1y", "2y"], default="1y", required=False)
    deposit_rate = serializers.FloatField(required=False, allow_null=True)

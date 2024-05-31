from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'weight']


class ConsumptionSerializer(serializers.Serializer):
    daily_goal = serializers.FloatField()
    remaining_goal = serializers.FloatField()
    consumption_percentage = serializers.FloatField()
    total_consumption = serializers.FloatField()
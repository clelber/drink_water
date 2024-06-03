from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'weight']


class ConsumptionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    weight = serializers.FloatField()
    daily_goal = serializers.FloatField()
    remaining_goal = serializers.FloatField()
    consumption_percentage = serializers.FloatField()
    total_consumption = serializers.FloatField()
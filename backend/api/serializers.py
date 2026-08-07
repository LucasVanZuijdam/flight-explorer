from rest_framework import serializers
from flights.models import Airport, FlightSearch


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = [
            "id",
            "iata_code",
            "name",
            "city",
            "country",
        ]

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightSearch
        fields = [
            "id",
            "origin",
            "departure_date",
            "return_date",
            "max_price",
            "created_at",
        ]
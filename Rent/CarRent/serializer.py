from rest_framework import serializers
from .models import Car, Rent, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id","name", "city", "address"]

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields =[
            "id",
            "brand",
            "model",
            "year",
            "daily_price",
            "transmission",
            "fuel_type",
            "seats",
            "is_active",
            "image"
        ]


class RentSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    pickup_location = LocationSerializer(read_only=True)
    dropoff_location = LocationSerializer(read_only=True)

    class Meta:
        model = Rent
        fields = [
            "id",
            "car",
            "pickup_location",
            "dropoff_location",
            "start_date",
            "end_date",
            "status",
            "total_price",
            "created_at",
        ]
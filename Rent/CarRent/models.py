from django.db import models
from django.contrib.auth import get_user_model
from .constants import (
    TRANSMISSION_CHOICES,
    FUEL_CHOICES,
    STATUS_CHOICES,
)
User = get_user_model()

class Location(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=256)
    def __str__(self):
        return f"{self.name} - {self.city} = {self.address}"

class Car(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    daily_price = models.DecimalField(max_digits=6, decimal_places=2)
    transmission = models.CharField(max_length=50, choices=TRANSMISSION_CHOICES)
    fuel_type = models.CharField(max_length=50, choices=FUEL_CHOICES)
    seats = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/', blank=True,null=True)


    def __str__(self):
        return f"{self.brand} - {self.model} - {self.year}"

class Rent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.PROTECT)
    pickup_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='pickup_location')
    dropoff_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='dropoff_location')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rent:{self.user} - {self.car}"

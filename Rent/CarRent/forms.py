from datetime import date

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Rent


class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = [
            "car",
            "pickup_location",
            "dropoff_location",
            "start_date",
            "end_date",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()

        car = cleaned_data.get("car")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date >= end_date:
                raise ValidationError("End date must be after start date.")
            if start_date < date.today():
                raise ValidationError("Start date cannot be in the past.")

        if car and start_date and end_date:
            overlapping = Rent.objects.filter(
                car=car,
                start_date__lt=end_date,
                end_date__gt=start_date,
                status__in=["pending", "confirmed"],
            )

            if self.instance.pk:
                overlapping = overlapping.exclude(pk=self.instance.pk)

            if overlapping.exists():
                raise ValidationError("This car is already rented for these dates.")

        return cleaned_data

    def calculate_total_price(self):
        car = self.cleaned_data["car"]
        start_date = self.cleaned_data["start_date"]
        end_date = self.cleaned_data["end_date"]
        days = (end_date - start_date).days
        return car.daily_price * days


User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

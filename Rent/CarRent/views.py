from copyreg import constructor

from django.shortcuts import render
from .forms import RentForm, RegisterForm
# Create your views here.
from decimal import Decimal
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Car,Location,Rent
from django.contrib.auth.forms import UserCreationForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CarSerializer, RentSerializer
def car_list(request):
    q = Car.objects.filter(is_active=True)
    brand = request.GET.get("brand")
    transmission = request.GET.get("transmission")
    fuel_type = request.GET.get("fuel_type")
    seats = request.GET.get("seats")
    max_price = request.GET.get("max_price")
    if brand:
        q = q.filter(brand__icontains=brand)
    if transmission:
        q = q.filter(transmission__icontains=transmission)
    if fuel_type:
        q = q.filter(fuel_type__icontains=fuel_type)

    if seats:
        try :
            q = q.filter(seats = int(seats))
        except ValueError:
            pass
    if max_price:
        try:
            q = q.filter(daily__price__lte = Decimal(max_price))
        except ValueError:
            pass
    q = q.order_by("daily_price", "brand", "model")
    context = {"cars":q}
    return render(request, "cars/car_list.html", context)

def car_detail(request, car_id:int):
    car = get_object_or_404(Car, pk=car_id, is_active=True)
    return render(request, "cars/car_detail.html", {"car":car})
@login_required
def rent_create(request):
    init = {}
    car_id = request.GET.get("car")
    if car_id:
        try:
            init["car"] = Car.objects.get(pk=car_id, is_active = True)
        except (ValueError, Car.DoesNotExist):
            pass
    if request.method == "POST":
        form = RentForm(request.POST)
        if form.is_valid():
            rent: Rent = form.save(commit=False)
            rent.user = request.user
            rent.total_price =  form.calculate_total_price()
            rent.status = "pending"
            rent.save()
            messages.success(request, "Successfully created rent.")
            return redirect("CarRent:my_rents")
        else:
            messages.error(request, "Please correct the errors.")
    else:
        form = RentForm(initial=init)
    return render(request, "rent/rent_form.html", {"form":form})
@login_required
def my_rents(request):
    rents = Rent.objects.filter(user=request.user).select_related("car", "pickup_location", "dropoff_location").order_by("-created_at")
    return render(request, "rent/my_rents.html", {"rents":rents})
@login_required
def rent_edit(request, rent_id:int):
    rent = get_object_or_404(Rent, pk=rent_id, user=request.user)
    if rent.status in ("cancelled", "finished"):
        messages.error(request, "You cannot edit cancelled or finished rents.")
        return redirect("CarRent:my_rents")
    if request.method == "POST":
        form = RentForm(request.POST, instance=rent)
        if form.is_valid():
            rent = form.save(commit=False)
            rent.total_price = form.calculate_total_price()
            rent.save()
            messages.success(request, "Successfully updated rent.")
            return redirect("CarRent:my_rents")
        else:
            messages.error(request, "Please correct the errors.")
    else:
        form = RentForm(instance=rent)
    context = {"form":form, "is_edit":True}
    return render(request, "rent/rent_form.html",context )
@login_required
def rent_cancel(request, rent_id:int):
    rent = get_object_or_404(Rent, pk=rent_id, user=request.user)
    rent.status = "cancelled"
    rent.save(update_fields=["status"])
    messages.success(request, "Successfully Cancelled rent.")
    return redirect("CarRent:my_rents")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. You can now log in.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("CarRent:car_list")


#Api
@api_view(["GET"])
def api_car_list(request):
    cars = Car.objects.filter(is_active=True).order_by("brand", "model")
    return Response(CarSerializer(cars, many=True).data)
@api_view(["GET"])
def api_my_rents(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required"}, status=401)

    rents = Rent.objects.filter(user=request.user).order_by("-created_at")
    serializer = RentSerializer(rents, many=True)
    return Response(serializer.data)





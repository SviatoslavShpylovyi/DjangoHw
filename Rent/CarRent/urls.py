from django.urls import path
from . import views
app_name = "CarRent"
urlpatterns = [
    path("cars/", views.car_list, name="car_list"),
    path("cars/<int:car_id>", views.car_detail, name="car_detail"),
    path("rent/create", views.rent_create, name="rent_create"),
    path("rent/my", views.my_rents, name="my_rents"),
    path("rent/<int:rent_id>/edit", views.rent_edit, name="rent_edit"),
    path("rent/<int:rent_id>/delete", views.rent_cancel, name="rent_cancel"),
    path("register/", views.register, name="register"),
    path("api/cars/", views.api_car_list, name="api_cars"),
    path("api/my-rents/", views.api_my_rents, name="api_my_rents"),
    path("logout/", views.logout_user, name="logout"),
]


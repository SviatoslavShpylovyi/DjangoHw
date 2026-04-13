import os
import random
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management import BaseCommand
from django.utils import timezone

from faker import Faker

from CarRent.models import Rent, Car, Location
from CarRent.constants import CAR_BRANDS, TRANSMISSION_CHOICES, FUEL_CHOICES, STATUS_CHOICES

transmissions = [v for v, _ in TRANSMISSION_CHOICES]
fuels = [v for v, _ in FUEL_CHOICES]
statuses = [v for v, _ in STATUS_CHOICES]

fake = Faker()

class Command(BaseCommand):
    help = "Generates fake data for the CarRent"
    def add_arguments(self, parser):
        parser.add_argument("--u", type=int, default =3)
        parser.add_argument("--l", type=int, default =5)
        parser.add_argument("--c", type=int, default=15)
        parser.add_argument("--r", type=int, default=10)
    def handle(self, *args, **options):
        User = get_user_model()
        users_count = options["u"]
        locs_count = options["l"]
        cars_count = options["c"]
        rents_count = options["r"]
        self.stdout.write("Generating fake data...")

        users = list(User.objects.all())
        if len(users) < users_count:
            for i in range(users_count - len(users)):
                username = fake.user_name()
                user = User.objects.create(username=username, password="1234", email=f'{username}@fake.net')
                users.append(user)

        locations = []
        for l in range(locs_count):
            locations.append(Location.objects.create(name=f"{fake.city()}", city = fake.city(), address=fake.address()))
        cars = []
        brand_model = []
        for brand, model in CAR_BRANDS.items():
            for m in model:
                brand_model.append((brand, m))
        for _ in range(cars_count):
            brand, model = random.choice(brand_model)

            images_dir = os.path.join(settings.MEDIA_ROOT, "seed_images")
            available_images = []
            if os.path.exists(images_dir):
                for file_name in os.listdir(images_dir):
                    file_path = os.path.join(images_dir, file_name)
                    if os.path.isfile(file_path) and file_name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                        available_images.append(file_name)
            car = Car(
                brand=brand,
                model=model,
                year=random.randint(2013, 2025),
                daily_price=random.randint(200, 600),
                transmission=random.choice(transmissions),
                fuel_type=random.choice(fuels),
                seats=random.choice([2, 4]),
                is_active=True,
            )

            if available_images:
                random_image_name = random.choice(available_images)
                random_image_path = os.path.join(images_dir, random_image_name)

                with open(random_image_path, "rb") as f:
                    car.image.save(
                        random_image_name,
                        ContentFile(f.read()),
                        save=False
                    )

            car.save()
            cars.append(car)
        today = timezone.localdate()
        for r in range(rents_count):
            start = today + timedelta(days=random.randint(-10, 20))
            end = start + timedelta(days=random.randint(1, 14))
            car = random.choice(cars)
            pickup = random.choice(locations)
            dropoff = random.choice(locations)
            days = (end - start).days
            total = car.daily_price * days
            Rent.objects.create(
                user = random.choice(users),
                car = car,
                pickup_location = pickup,
                dropoff_location = dropoff,
                start_date = start,
                end_date = end,
                status = random.choice(statuses),
                total_price = total,
            )

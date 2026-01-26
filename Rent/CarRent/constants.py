CAR_BRANDS = {
    "Toyota": ["Corolla", "Camry", "Yaris"],
    "BMW": ["3_Series", "5_Series", "X3"],
    "Renault": ["Clio", "Megane", "Captur"],
    "Peugeot": ["208"],
    "Tesla": ["Model_3", "Model_Y"],
}

BRAND_CHOICES = [(b, b) for b in CAR_BRANDS.keys()]
MODEL_CHOICES = [(m, m) for models in CAR_BRANDS.values() for m in models]

TRANSMISSION_CHOICES = [
    ("Manual", "Manual"),
    ("Automatic", "Automatic"),
]

FUEL_CHOICES = [
    ("Petrol", "Petrol"),
    ("Diesel", "Diesel"),
    ("Hybrid", "Hybrid"),
    ("Electric", "Electric"),
]

STATUS_CHOICES = [
    ("pending", "pending"),
    ("confirmed", "confirmed"),
    ("cancelled", "cancelled"),
    ("finished", "finished"),
]
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    description: str
    price: str

class Products:
    BACKPACK = Product(
        name="Sauce Labs Backpack",
        description="carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop protection.",
        price="$29.99"
    )
    BIKE_LIGHT = Product(
        name="Sauce Labs Bike Light",
        description="A red light isn't the only thing your bike needs.",
        price="$9.99"
    )
    # Can add more as needed

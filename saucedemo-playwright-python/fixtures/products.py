from dataclasses import dataclass

@dataclass
class Product:
    name: str
    description: str
    price: str
    image_url: str

class Products:
    BACKPACK = Product(
        name="Sauce Labs Backpack",
        description="carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.",
        price="$29.99",
        image_url="https://www.saucedemo.com/static/media/sauce-backpack-1200x1500.0a0b85a385945026062b.jpg"
    )
    BIKE_LIGHT = Product(
        name="Sauce Labs Bike Light",
        description="A red light isn't the desired state in testing but it sure helps when riding your bike at night. Water-resistant with 3 lighting modes, 1 AAA battery included.",
        price="$9.99",
        image_url="https://www.saucedemo.com/static/media/bike-light-1200x1500.37c843b09a7d77409d63.jpg"
    )
    BOLT_TSHIRT = Product(
        name="Sauce Labs Bolt T-Shirt",
        description="Get your testing superhero on with the Sauce Labs bolt T-shirt. From American Apparel, 100% ringspun combed cotton, heather gray with red bolt.",
        price="$15.99",
        image_url="https://www.saucedemo.com/static/media/bolt-shirt-1200x1500.c2599ac5f0a35ed5931e.jpg"
    )
    FLEECE_JACKET = Product(
        name="Sauce Labs Fleece Jacket",
        description="It's not every day that you come across a midweight quarter-zip fleece jacket capable of handling everything from a relaxing day outdoors to a busy day at the office.",
        price="$49.99",
        image_url="https://www.saucedemo.com/static/media/sauce-pullover-1200x1500.51d7ffaf301e698772c8.jpg"
    )
    ONESIE = Product(
        name="Sauce Labs Onesie",
        description="Rib snap infant onesie for the junior automation engineer in development. Reinforced 3-snap bottom closure, two-needle hemmed sleeved and bottom won't unravel.",
        price="$7.99",
        image_url="https://www.saucedemo.com/static/media/red-onesie-1200x1500.2ec615b271ef4c3bc430.jpg"
    )
    TEST_ALL_THE_THINGS_TSHIRT = Product(
        name="Test.allTheThings() T-Shirt (Red)",
        description="This classic Sauce Labs t-shirt is perfect to wear when cozying up to your keyboard to automate a few tests. Super-soft and comfy ringspun combed cotton.",
        price="$15.99",
        image_url="https://www.saucedemo.com/static/media/red-tatt-1200x1500.30dadef477804e54fc7b.jpg"
    )

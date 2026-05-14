import random
import string

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

def get_price_value(price_string: str) -> float:
    """Converts '$29.99' to 29.99"""
    return float(price_string.replace('$', '').replace('Item total: ', '').replace('Total: ', '').replace('Tax: ', '').strip())

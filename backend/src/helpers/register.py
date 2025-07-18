import random


def generate_pin() -> str:
    return str(random.randint(1000, 9999))
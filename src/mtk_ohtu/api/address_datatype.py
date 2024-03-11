from dataclasses import dataclass

@dataclass
class Address():
    latitude: float
    longitude: float
    country: str
    city: str
    state: str
    streetAddress: str
    postalCode: str
    apartment: str

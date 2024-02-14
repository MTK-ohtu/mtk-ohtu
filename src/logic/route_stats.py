from enum import Enum

"""Route satistic logic module."""

class FuelType(Enum):
    PETROL = 2.31
    DIESEL = 2.68
    BIODIESEL = 2.0
    NATURAL_GAS = 2.75
    BIO_GAS = 1.97
    ELECTRICITY = 0.0


def calculate_emissions(fuel: FuelType, fuel_efficiency, distance):
    """Return route emissions.
    
    Args:
        fuel: fuel type
        fuel_efficiency: fuel consuption per 100 km
    """
    return distance/100000*fuel_efficiency*fuel.value

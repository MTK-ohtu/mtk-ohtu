from enum import Enum

"""Route satistic logic module."""

class FuelType(Enum):
    PETROL = 2.31
    DIESEL = 2.68
    BIODIESEL = 2.0
    NATURAL_GAS = 2.75
    BIO_GAS = 1.97
    ELECTRICITY = 0.0


def calculate_emissions(fuel, distance, fuel_efficiency = 55.0):
    """Return route emissions (kg CO2).
    
    Args:
        fuel: fuel type
        fuel_efficiency: fuel consuption per 100 km
    """
    print(f'fuel: {fuel}, distance: {distance}, fuel_efficiency: {fuel_efficiency}')

    fuels = {
        "diesel": FuelType.DIESEL,
        "petrol": FuelType.PETROL,
        "biodiesel": FuelType.BIODIESEL,
        "natural_gas": FuelType.NATURAL_GAS,
        "bio_gas": FuelType.BIO_GAS,
        "electricity": FuelType.ELECTRICITY,
    }
    if fuel in fuels.keys():
        fuel = fuels[fuel]


    if type(fuel_efficiency) != float:
        if type(fuel_efficiency) == int:
            fuel_efficiency = float(fuel_efficiency)
        elif type(fuel_efficiency) == str:
            if fuel_efficiency == "":
                fuel_efficiency = 55.0
            else:
                try:
                    fuel_efficiency = float(fuel_efficiency)
                except:
                    raise ValueError(f"fuel_efficiency ({fuel_efficiency}) string conversion to float failed")
        #raise ValueError("fuel_efficiency must be a float. Not a " + str(type(fuel_efficiency)))

    return distance/100000*float(fuel_efficiency)*fuel.value

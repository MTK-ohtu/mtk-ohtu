"""Route satistic logic module."""
from enum import Enum


class FuelType(Enum):
    PETROL = 2.31
    DIESEL = 2.68
    BIODIESEL = 2.0
    NATURAL_GAS = 2.75
    BIO_GAS = 1.97
    ELECTRICITY = 0.04


class Emissions:
    """Emissions class."""

    def __init__(self, fuel, distance, fuel_efficiency=55.0):
        """Init."""
        self.fuel = fuel
        self.distance = distance
        self.fuel_efficiency = self.validate_fuel_efficiency(fuel_efficiency)
        self.fuels = {
            "diesel": FuelType.DIESEL,
            "petrol": FuelType.PETROL,
            "biodiesel": FuelType.BIODIESEL,
            "natural_gas": FuelType.NATURAL_GAS,
            "biogas": FuelType.BIO_GAS,
            "electricity": FuelType.ELECTRICITY,
        }

    def validate_fuel_efficiency(self, fuel_efficiency):
        """Validate fuel efficiency."""
        if not isinstance(fuel_efficiency, float):
            if isinstance(fuel_efficiency, str):
                if fuel_efficiency == "":
                    fuel_efficiency = 55.0
                else:
                    try:
                        fuel_efficiency = float(fuel_efficiency)
                    except Exception as exept:
                        raise ValueError(
                            f"fuel_efficiency ({fuel_efficiency}) string conversion to float failed"
                        ) from exept
            else:
                try:
                    fuel_efficiency = float(fuel_efficiency)
                except Exception as exept:
                    raise ValueError(
                        "fuel_efficiency must be a float. Not a "
                        + str(type(fuel_efficiency))
                    ) from exept
        return fuel_efficiency

    def calculate_emissions(self, fuel=None):
        """Return route emissions (kg CO2)."""

        if fuel is None:
            fuel = self.fuel

        if fuel in self.fuels.keys():
            fuel = self.fuels[fuel]

        return round(self.distance / 100000 * float(self.fuel_efficiency) * fuel.value)

    def get_emissions_for_all_fuels(self):
        """Return emissions for all fuel types."""
        emissions = {}
        for fuel in self.fuels.keys():
            emissions[fuel] = self.calculate_emissions(fuel)
        return emissions

from geopy.geocoders import Nominatim
from config import NOMINATIM_DOMAIN, NOMINATIM_USER_AGENT

geolocator = Nominatim(domain=NOMINATIM_DOMAIN, user_agent=NOMINATIM_USER_AGENT, scheme="http")


class Location:
    """A class for storing location information for an address, including latitude and longitude.

    Attributes:
        location (Location): The location of the address.
        latitude (float): The latitude of the address.
        longitude (float): The longitude of the address.
    """

    def __init__(self, loc_input):
        """Initialize the Location class.

        Args:
            loc_input (str or tuple or list): The address or coordinates of the location.
        """
        if type(loc_input) == str:
            self.location = self.location_from_address(loc_input)
            self.longitude = self.location.longitude
            self.latitude = self.location.latitude
        elif type(loc_input) == tuple or type(loc_input) == list:
            self.location = None
            self.longitude = loc_input[0]
            self.latitude = loc_input[1]
        else:
            raise ValueError("Invalid input")

    def location_from_address(self, address):
        """Return the coordinates of the address."""
        try:
            return geolocator.geocode(address)
        except:
            raise ValueError(f"Invalid address: {address}")

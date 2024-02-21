from geopy.geocoders import Nominatim
from ..config import NOMINATIM_DOMAIN, NOMINATIM_USER_AGENT

geolocator = Nominatim(
    domain=NOMINATIM_DOMAIN, user_agent=NOMINATIM_USER_AGENT, scheme="http"
)


class Location:
    """A class for storing location information for an address, including latitude and longitude.

    Attributes:
        location (Location): The location of the address.
        latitude (float): The latitude of the address.
        longitude (float): The longitude of the address.
    """

    def __init__(self, loc_input: str | tuple | list):
        """Initialize the Location class.

        Args:
            loc_input (str or tuple or list): The address or coordinates of the location.
                If coordinates, then the format is (longitude, latitude)
        """
        if type(loc_input) == str:
            self.location = self._location_from_address(loc_input)
            self.longitude = self.location.longitude
            self.latitude = self.location.latitude
        elif type(loc_input) == tuple or type(loc_input) == list:
            self.location = None
            self.longitude = loc_input[0]
            self.latitude = loc_input[1]
        else:
            raise ValueError("Invalid location input")

    def _location_from_address(self, address):
        """Return the coordinates of the address."""
        try:
            loc = geolocator.geocode(address)
            if loc is None:
                raise ValueError(f"No result found for address {address}")
            return loc
        except:
            raise ValueError(f"Invalid address: {address}")

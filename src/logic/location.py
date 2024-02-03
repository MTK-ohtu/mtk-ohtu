from geopy.geocoders import Nominatim

class Location:
    """A class for storing location information for an address, including latitude and longitude.

    Attributes:
        location (Location): The location of the address.
        latitude (float): The latitude of the address.
        longitude (float): The longitude of the address.
    """

    def __init__(self, loc_input, user_email = "miko.paajanen@helsinki.fi"):
        """Initialize the Location class.

        Args:
            loc_input (str or tuple or list): The address or coordinates of the location.
            user_email (str): The email address used for the API call.
        """
        self.geolocator = Nominatim(user_agent=user_email)
        if type(loc_input) == str:
            self.location = self.location_from_address(loc_input)
            self.longitude = self.location.longitude
            self.latitude = self.location.latitude            
        elif type(loc_input) == tuple or type(loc_input) == list:
            self.location = None
            self.longitude = loc_input[0]
            self.latitude = loc_input[1]
            


    def location_from_address(self, address):
        """Return the coordinates of the address."""
        try:
            return self.geolocator.geocode(address)
        except:
            raise ValueError(f"Invalid address: {address}")

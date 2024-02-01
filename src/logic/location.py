from geopy.geocoders import Nominatim

class Location:
    """A class for storing the latitude and longitude of a location.

    Attributes:
        location (Location): The location of the address.
        latitude (float): The latitude of the address.
        longitude (float): The longitude of the address.
    """

    def __init__(self, address, user_email = "miko.paajanen@helsinki.fi"):
        """Initialize the Location class.

        Args:
            address (str): The address of the location.
            user_email (str): The email address used for the API call.
        """
        geolocator = Nominatim(user_agent=user_email)
        self.location = geolocator.geocode(address)
        self.latitude = self.location.latitude
        self.longitude = self.location.longitude

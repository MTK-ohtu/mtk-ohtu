class Location:
    """A class for storing the latitude and longitude of a location.

    Attributes:
        location (Location): The location of the address.
        latitude (float): The latitude of the address.
        longitude (float): The longitude of the address.
    """

    def __init__(self, address, geolocator):
        """Initialize the Location class.

        Args:
            address (str): The address of the location.
            geolocator (geopy.geocoders.Nominatim): The geolocator object.
        """
        self.location = geolocator.geocode(address)
        self.latitude = self.location.latitude
        self.longitude = self.location.longitude

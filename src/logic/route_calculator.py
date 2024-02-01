import geopy.distance
import requests
from logic.location import Location
import datetime


class Route:

    """A class for calculating the distance and duration of a route between two locations.

    Attributes:
        location1 (Location): The starting location of the route.
        location2 (Location): The ending location of the route.
        api_key (str): The API key used for the API call.
        distance (int): The distance of the route in meters.
        duration (int): The duration of the route in seconds.

    """

    def __init__(
        self,
        start,
        end,
        user_email="miko.paajanen@helsinki.fi",
        key="5b3ce3597851110001cf6248179f16aaf79a4d89aaeae99d8a17421b",
    ):
        """Initialize the Route class.

        Args:
            start (str): The starting location of the route.
            end (str): The ending location of the route.
            user_email (str): The email address used for the API call.
            key (str): The API key used for the API call.
        """
        print("Route init")
        self.location1 = Location(start, user_email)
        self.location2 = Location(end, user_email)
        self.api_key = key
        route_summary = self.__get_route_summary()
        self.distance = route_summary["distance"]  # Distance in meters
        self.duration = route_summary["duration"]  # Duration in seconds
        try:
            self.geojson = self.__get_route_call().text
        except:
            self.geojson = None

    def geodesic_distance(self):
        """Return the geodesic distance (bee-line) between the two locations in kilometers."""
        return geopy.distance.geodesic(
            (self.location1.latitude, self.location1.longitude),
            (self.location2.latitude, self.location2.longitude),
        ).m

    def __get_route_call(self):
        """Return the route call from the openrouteservice API."""
        headers = {
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        }
        call = requests.get(
            f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={self.api_key}&start={self.location1.longitude},%20{self.location1.latitude}&end={self.location2.longitude},%20{self.location2.latitude}%20",
            headers=headers,
        )
        if call.status_code != 200:
            return f"error: {call.status_code}"
        else:
            return call

    def __get_route_summary(self):
        """Return the route summary from the openrouteservice API."""
        try:
            call = self.__get_route_call()
            return call.json()["features"][0]["properties"]["summary"]
        except:
            return {"distance": 0, "duration": 0}
    
    def __get_route_waypoints(self):
        call = self.__get_route_call()
        return call.json()["features"][0]["geometry"]["coordinates"]


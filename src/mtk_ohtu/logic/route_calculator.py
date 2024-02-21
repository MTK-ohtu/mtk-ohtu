import geopy.distance
import requests
from ..logic.location import Location
import datetime
from enum import Enum
from flask import session


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
        start: Location,
        end: Location,
        key="5b3ce3597851110001cf6248179f16aaf79a4d89aaeae99d8a17421b",
    ):
        """Initialize the Route class.

        Args:
            start (Location): The starting location of the route.
            end (Location): The ending location of the route.
            user_email (str): The email address used for the API call.
            key (str): The API key used for the API call.
        """

        self.location1 = start
        self.location2 = end
        if (
            self.location1.latitude == self.location2.latitude
            and self.location1.longitude == self.location2.longitude
        ):
            raise ValueError("The locations are the same.")
        self.api_key = key
        self.distance = 0  # Distance in meters
        self.duration = 0  # Duration in seconds
        self.geodesic_distance_meters = 0  # Geodesic distance in meters
        self.geojson = None

    def calculate_route(self):
        """Calculate the route between the two locations. The route detailes are saved as class variables."""
        print("getting route")
        try:
            call = self.__get_route_call()
            route_summary = call.json()["features"][0]["properties"]["summary"]
            self.geojson = call.text
        except:
            raise ValueError("Error in route call")

        # if the two locations are the same, the summary is an empty dict
        if "distance" not in route_summary:
            self.distance = 0
            self.duration = 0
        else:
            self.distance = route_summary["distance"]
            self.duration = route_summary["duration"]

    def geodesic_distance(self) -> float:
        """Return the geodesic distance (bee-line) between the two locations in meters."""
        self.geodesic_distance_meters = geopy.distance.geodesic(
            (self.location1.latitude, self.location1.longitude),
            (self.location2.latitude, self.location2.longitude),
        ).m
        return self.geodesic_distance_meters

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



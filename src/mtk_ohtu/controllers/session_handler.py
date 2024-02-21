from flask import Flask, session
from flask_session import Session
import datetime

""" A module for handling session data. """

def save_route_to_session(route):
    """Saves the route details to the session."""
    session['route_details'] = {
        'distance': round(route.distance / 1000, 1),
        'duration': str(
                datetime.timedelta(seconds=(round(route.duration)))
            ),
        "location1": {"location":route.location1.location, "longitude":route.location1.longitude, "latitude":route.location1.latitude},
        "location2": {"location":route.location2.location, "longitude":route.location2.longitude, "latitude":route.location2.latitude},
        # "geodesic_distance_meters": route.geodesic_distance_meters,
        "route_geojson": route.geojson
    }

def get_route_from_session():
    """Returns the route details from the session."""
    return session.get('route_details')

def delete_route_from_session():
    """Deletes the route details from the session."""
    session.pop('route_details', None)


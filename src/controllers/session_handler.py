from flask import Flask, session

""" A module for handling session data. """

def save_route_to_session(route):
    """Saves the route details to the session."""
    session['route_details'] = {
        'distance': route.distance,
        'duration': route.duration,
        "location1": (route.location1.longitude, route.location1.latitude),
        "location2": (route.location2.longitude, route.location2.latitude),
        # "geodesic_distance_meters": route.geodesic_distance_meters,
        # "geojson": route.geojson
    }

def get_route_from_session():
    """Returns the route details from the session."""
    return session.get('route_details')

def delete_route_from_session():
    """Deletes the route details from the session."""
    session.pop('route_details', None)


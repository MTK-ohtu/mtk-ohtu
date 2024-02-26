from ..database.db_datastructs import Listing
from ..logic.location import Location
from ..database.db_datastructs import LogisticsNode
from .route_calculator import Route
from ..database.database import db_get_logistics
from ..config import DATABASE_POOL


def get_logistics_info(listing: Listing, user_location: Location) -> tuple[float, int]:
    """Gets the necessary logistics info for API3 when supplied the listing and the location of the user.

    Args:
        listing (Listing): the listing / posting / item / sidestream source / etc. in question,
        location (Location): the location of the user, according to which to calculate the

    Returns:
        a tuple: (float: the distance from the listing to the user in km, int: the number of available logistics providers)
    """

    route = Route(listing.location, user_location)
    route.calculate_route()

    providers = get_logistics_providers(listing, user_location)

    return (float(route.distance) / 1000.0, len(providers))


def get_logistics_providers(
    listing: Listing, user_location: Location
) -> list[LogisticsNode]:
    """Gets the available logistics providers / nodes for the user's location & listing

    Args:
        listing (Listing): the listing in question,
        location (Location): the buyer's location,

    Returns:
        a list of LogisticsNodes
    """

    nodes = db_get_logistics(DATABASE_POOL)
    accepted = []

    for node in nodes:
        route_to_listing = Route(listing.location, node.location)
        if route_to_listing.geodesic_distance() / 1000.0 <= node.delivery_radius:
            route_to_user = Route(user_location, node.location)
            if route_to_user.geodesic_distance() / 1000.0 <= node.delivery_radius:
                accepted.append(node)

    return accepted

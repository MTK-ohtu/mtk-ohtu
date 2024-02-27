import logging
import mtk_ohtu.database.db_contractors
from ..database import db_cargo as db
from ..config import DATABASE_POOL
from ..logic.location import Location as l


def add_contractor(user_id, name, business_id):
    """
    Adds a new contractor
    Args:
        user_id: user id
        name: name of contractor
        business_id: business id if needed
    Returns:
        id if adding is complete
        else False
    """
    try:
        id = mtk_ohtu.database.db_contractors.db_add_contractor(user_id, name, business_id, pool=DATABASE_POOL)
        return id
    except Exception as er:
        logging.error(er)
        return False


def add_contractor_location(
        contractor_id,
        address,
        postcode,
        city,
        telephone,
        email,
        radius,        
):
    """
    Adds a new location for a contractor
    Args:
        contractor_id: contractor id
        address: location address
        telephone: telephone number
        email: email address
        radius: delivery radius, -1 if not specified
    Returns:
        id if adding is complete
        else False
    """
    location = f"{address}, {postcode}, {city}"
    try:
        coordinates = l(location)
        lon = coordinates.longitude
        lat = coordinates.latitude
        id = mtk_ohtu.database.db_contractors.db_add_contractor_location(
            contractor_id,
            address,
            telephone,
            email,
            lon,
            lat,
            radius,
            pool=DATABASE_POOL,
        )
        return id
    except Exception as er:
        logging.error(er)
        return False


def add_cargo_capability(
    contractor_location_id,
    categories,
    base_rates,
    prices_per_hour,
    max_capacities,
    max_distances,
):
    """
    Adds all deliverable sidestreams for contractor location
    Args:
        contractor_location_id: contractor location id
        categories: sidestream categories
        base_rates: base rates for sidestreams
        prices_per_hour: prices for sidestreams
        max_capacities: maximum capacities for sidestreams
        max_distances: maximum delivery distances for sidestreams
    Returns:
        True if adding is complete
        else False
    """
    try:
        for i,category in enumerate(categories):
            cargo_type = category
            price = prices_per_hour[i]
            base_rate = base_rates[i]
            max_capacity = max_capacities[i]
            max_distance = max_distances[i]

            db.db_add_cargo_capability(
                contractor_location_id,
                cargo_type,
                price,
                base_rate,
                max_capacity,
                max_distance,
                pool=DATABASE_POOL,
            )
    except:
        return False
    return True


def get_locations_and_cargo_capability(contractor_id):
    """
    Creates an array of contractor's locations and available cargo capabilities
    Args:
        contractor_id: contractor's identifying number

    Returns:
        array of tuples: (LogisticsNode, [CargoTypeInfo])
    """
    locations = contractor_locations(contractor_id)

    capability = []
    for location in locations:
        capability.append((location, cargo_capability(location.id)))

    return capability


def contractor_locations(contractor_id):
    """
    Returns contractor's locations on a list
    """
    return mtk_ohtu.database.db_contractors.db_get_contractor_locations(contractor_id, DATABASE_POOL)


def cargo_capability(contractor_location_id):
    """
    Returns a list of locations cargo hauling capabilities
    """
    return db.db_get_location_cargo_capabilities(contractor_location_id, DATABASE_POOL)

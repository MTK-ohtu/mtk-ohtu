import logging
from flask import session
from ..database import db_contractors
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
        id = db_contractors.db_add_contractor(
            user_id, name, business_id, pool=DATABASE_POOL
        )
        return id
    except Exception as er:
        logging.error(er)
        return False


def add_contractor_location(
    contractor_id, address, postcode, city, telephone, email, radius, description
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
        id = db_contractors.db_add_contractor_location(
            contractor_id,
            address,
            telephone,
            email,
            lon,
            lat,
            radius,
            description,
            pool=DATABASE_POOL,
        )
        return id
    except Exception as er:
        logging.error(er)
        return False
    
def add_eco_type(contractor_location_id, eco_type):
    db_contractors.db_add_eco_type(
        contractor_location_id,
        eco_type,
        pool=DATABASE_POOL
    )

def modify_contractor_location(
    location_id, address, postcode, city, telephone, email, radius, description
):
    """
    Updates contractor location information
    Args:
        location_id: locations identifying number
        address: location address
        postcode: location postcode
        city: location city
        telephone: telephone number
        email: email address
        radius: delivery radius
        description: location summary
    Returns:
        bool: True if modified successfully, otherwise False
    """
    location = f"{address}, {postcode}, {city}"
    try:
        coordinates = l(location)
        longitude = coordinates.longitude
        latitude = coordinates.latitude
    except:
        return False

    return db_contractors.db_modify_contractor_location(
        location_id,
        address,
        telephone,
        email,
        longitude,
        latitude,
        radius,
        description,
        DATABASE_POOL,
    )


def remove_contractor_location(location_id):
    """
    Removes location and all data connected to it
    Args:
        location_id: locations identifying number
    """
    locations_cargo = cargo_capability(location_id)
    for cargo in locations_cargo:
        db.db_remove_cargo_capability(cargo.id, DATABASE_POOL)

    return db_contractors.db_remove_contractor_location(location_id, DATABASE_POOL)


def add_cargo_capability(
    contractor_location_id,
    category,
    base_rate,
    price_per_hour,
    max_capacity,
    max_distance,
    unit,
    can_process,
    description,
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
    if can_process == None:
        can_process = False
    if base_rate == "":
        base_rate = -1
    if price_per_hour == "":
        price_per_hour = -1
    if max_capacity == "":
        max_capacity = -1
    try:
        db.db_add_cargo_capability(
            contractor_location_id,
            category,
            price_per_hour,
            base_rate,
            max_capacity,
            max_distance,
            unit,
            can_process,
            description,
            pool=DATABASE_POOL,
        )
    except Exception as ex:
        logging.warning(ex)
        return False
    return True


def remove_cargo_capability(contractor_id, cargo_id):
    """
    Removes a deliverable sidestream
    Args:
        contractor_id: contractor's identifying number
        cargo_id: sidestreams identifying number
    Returns:
        bool: True if succeeds, False otherwise
    """
    if not check_asset_ownership("cargo", cargo_id, contractor_id):
        return False

    return db.db_remove_cargo_capability(cargo_id, DATABASE_POOL)


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
    return db_contractors.db_get_contractor_locations(contractor_id, DATABASE_POOL)


def cargo_capability(contractor_location_id):
    """
    Returns a list of locations cargo hauling capabilities
    """
    return db.db_get_location_cargo_capabilities(contractor_location_id, DATABASE_POOL)


def check_asset_ownership(asset_type, asset_id, contractor_id):
    """
    Checks if given contractor matches the owner of given asset
    Args:
        asset_type: "location" or "cargo"
        asset_id: asset's identifying number
        contractor_id: contractor's identifying number
    Returns:
        bool: True if owner, False otherwise
    """
    if asset_type == "location":
        owner = db_contractors.db_get_contractor_location_owner(asset_id, DATABASE_POOL)
    elif asset_type == "cargo":
        owner = db.db_get_cargo_owner(asset_id, DATABASE_POOL)
    else:
        return False

    if contractor_id == owner:
        return True

    return False


def contractor_id():
    """
    Returns contractor's id number
    """
    return session.get("contractor_id", 0)

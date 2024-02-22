import logging
from ..database import database as db
from ..config import DATABASE_POOL
from ..logic.location import Location as l


def add_contractor(
    user_id,
    name,
    business_id
):
    """
    Adds a new logistic company and categories
    Args:
        service_type: company or private
        name: name of contractor
        business_id: business id if service_type is company
        address: address of contractor
        radius: how far contractor can deliver
        categories: categories of material the contractor is capable of delivering
        base_rates: base payments for different materials
        prices_per_hour: hourly prices for different materials
    Returns:
        Contractor id if adding is complete
        False if address is not correct
    """
    if not all(
        [
            user_id,
            name,
        ]
    ):
        return False

    id = db.db_add_contractor(
        user_id, name, business_id, pool=DATABASE_POOL
    )
    return id

def add_contractor_location(
        contractor_id,
        address,
        telephone,
        email,
        radius,        
):
    if radius == "":
        radius = -1
    try:
        coordinates = l(address)
        lon = coordinates.longitude
        lat = coordinates.latitude
        id = db.db_add_contractor_location(
            contractor_id, address, telephone, email, lon, lat, radius, pool=DATABASE_POOL
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
        max_distances
):
    for i in range(len(categories)):
            cargo_type = categories[i]
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
    return db.db_get_contractor_locations(contractor_id, DATABASE_POOL)

def cargo_capability(contractor_location_id):
    """
    Returns a list of locations cargo hauling capabilities
    """
    return db.db_get_location_cargo_capabilities(contractor_location_id, DATABASE_POOL)

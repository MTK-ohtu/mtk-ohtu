from ..database import database as db
from flask import session
from ..config import DATABASE_POOL
from ..logic.location import Location as l


def addlogistics(
        user_id,
        name, 
        business_id, 
        address, radius, 
        categories, 
        base_rates, 
        prices_per_hour, 
        max_capacities, 
        max_distances
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
        True if adding is complete
        False if address is not correct
    """
    if radius == "":
        radius = -1
    try:
        coordinates = l(address)
    except:
        return False
    lon = coordinates.longitude
    lat = coordinates.latitude

    id = db.db_add_logistics(
        user_id, name, business_id, address, lon, lat, radius, pool=DATABASE_POOL
    )
    for i in range(len(categories)):
        type = categories[i]
        price = prices_per_hour[i]
        base_rate = base_rates[i]
        max_capacity = max_capacities[i]
        max_distance = max_distances[i]
        db.db_add_cargo_category(
            id, type, price, base_rate, max_capacity, max_distance, pool=DATABASE_POOL
        )
    
    session["contractor_id"] = id
    return True

def contractor_id():
    return session["contractor_id"]

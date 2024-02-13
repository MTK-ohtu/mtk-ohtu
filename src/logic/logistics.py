from database import database as db
from flask import session
from config import DATABASE_POOL
from logic.location import Location as l


def addlogistics(service_type, name, business_id, address, radius, categories, base_rates, prices_per_hour):
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

    print("Service Type:", service_type)
    print("Name:", name)
    print("Business ID:", business_id)
    print("Address:", address)
    print("Longitude:", lon)
    print("Latitude:", lat)
    print("Radius:", radius)
    print("Categories", categories)
    print("Base rates:", base_rates)
    print("Prices:", prices_per_hour)

    id = db.db_add_logistics(
        name, business_id, address, lon, lat, radius, pool=DATABASE_POOL
    )
    i = 0
    while i < len(categories):
        type = categories[i]
        price = prices_per_hour[i]
        base_rate = base_rates[i]
        db.db_add_cargo_category(
            id, type, price, base_rate, pool=DATABASE_POOL
        )
        i += 1
    return True

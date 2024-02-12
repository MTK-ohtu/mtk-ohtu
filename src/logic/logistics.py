from database import database as db
from flask import session
from config import DATABASE_CONFIG
from logic.location import Location


def addlogistics(service_type, name, business_id, address, radius):
    """
    Adds a new logistic company

    In progress...
    """
    if radius == "":
        radius = -1

    

    print("Service Type:", service_type)
    print("Name:", name)
    print("Business ID:", business_id)
    print("Address:", address)
    print("Radius:", radius)
    
    id = db.db_add_logistics(
        name, business_id, address, radius, config=DATABASE_CONFIG
    )

    # db.db_add_vehicle(id, name, vehicle_category, max_weight, price_per_hour, config=DATABASE_CONFIG)

from database import database as db
from flask import session
from config import DATABASE_POOL
from location import Location as l


def addlogistics(
    service_type, name, business_id, address, vehicle_category, max_amount
):
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
    print("Vehicle Category:", vehicle_category)
    print("Max", max_amount)

    db.db_add_logistics(
        name, business_id, address, vehicle_category, pool=DATABASE_POOL
    )

    # db.db_add_vehicle(id, name, vehicle_category, max_weight, price_per_hour, config=DATABASE_CONFIG)

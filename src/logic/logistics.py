from database import database as db
from flask import session
from config import DATABASE_CONFIG


def addlogistics(service_type, name, business_id, address, vehicle_category, max_weight, price_per_hour):
    """
    Adds a new logistic company

    In progress...
    """
    print("Service Type:", service_type)
    print("Name:", name)
    print("Business ID:", business_id)
    print("Address:", address)
    print("Vehicle Category:", vehicle_category)
    print("Max", max_weight)
    print("Price/h", price_per_hour)
    
    id = db.db_add_logistics(
        name, business_id, address, config=DATABASE_CONFIG
    )

    db.db_add_vehicle(id, name, vehicle_category, max_weight, price_per_hour, config=DATABASE_CONFIG)

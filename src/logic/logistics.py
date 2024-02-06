from database import database as db
from flask import session
from config import DATABASE_CONFIG


def addlogistics(service_type, name, business_id, address, vehicle_categories):
    """
    Adds a new logistic company

    In progress...
    """
    print("Service Type:", service_type)
    print("Name:", name)
    print("Business ID:", business_id)
    print("Address:", address)
    print("Vehicle Categories:", vehicle_categories)

    db.db_add_logistics(name, business_id, address, vehicle_categories, config=DATABASE_CONFIG)
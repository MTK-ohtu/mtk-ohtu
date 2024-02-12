from database import database as db
from flask import session
from config import DATABASE_POOL


def addlogistics(service_type, name, business_id, address, vehicle_category, max_amount):
    """
    Adds a new logistic company

    In progress...
    """
    print("Service Type:", service_type)
    print("Name:", name)
    print("Business ID:", business_id)
    print("Address:", address)
    print("Vehicle Category:", vehicle_category)
    print("Max", max_amount)

    db.db_add_logistics(
        name, business_id, address, vehicle_category, config=DATABASE_POOL
    )

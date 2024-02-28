import logging
from psycopg_pool import ConnectionPool
from .db_enums import CategoryType
from .db_datastructs import CargoTypeInfo

# pylint: disable=E1129

def db_add_cargo_capability(
    cargo_id: int,
    cargo_type: CategoryType,
    price_per_hour: int,
    base_rate: int,
    max_capacity: int,
    max_distance: int,
    pool: ConnectionPool,
) -> bool:
    """
    Adds new categories of materials that the contractor are capable to transport
    Args:
        id: id of the logistics contractor
        type: product type
        price_per_hour: price per hour for product transportation
        base_rate: base payment for product transportation
        max_capacity: maximum capacity for a single product
    """
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO cargo_capabilities \
                (contractor_location_id, type, price_per_km, base_rate, max_capacity, max_distance) \
                VALUES (%s,%s,%s,%s,%s,%s)",
            (cargo_id, cargo_type, price_per_hour, base_rate, max_capacity, max_distance),
        )
        out = True
    return out


def db_get_location_cargo_capabilities(
    contractor_location_id: int, pool: ConnectionPool
) -> list[CargoTypeInfo]:
    """
    Gets a list of sidestreams the location is available to deliver
    Args:
        contractor_location_id: location's identifying number
        pool: a database connection

    Returns:
        a list of CargoTypeInfos
    """
    out = []
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM cargo_capabilities WHERE contractor_location_id=%s;",
            (contractor_location_id,)
        )
        out = cursor.fetchall()
    if not out:
        return []
    return [CargoTypeInfo(*x[1:]) for x in out]

import logging
from psycopg_pool import ConnectionPool
from .db_enums import CategoryType, BatchUnitsType
from .db_datastructs import CargoTypeInfo

# pylint: disable=E1129


def db_add_cargo_capability(
    cargo_id: int,
    cargo_type: CategoryType,
    price_per_hour: int,
    base_rate: int,
    max_capacity: int,
    max_distance: int,
    unit: BatchUnitsType,
    can_process: bool,
    description: str,
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
                (contractor_location_id, type, price_per_km, base_rate, max_capacity, max_distance, unit, can_process, description) \
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                cargo_id,
                cargo_type,
                price_per_hour,
                base_rate,
                max_capacity,
                max_distance,
                unit,
                can_process,
                description,
            ),
        )
        out = True
    return out


def db_remove_cargo_capability(cargo_id: int, pool: ConnectionPool) -> bool:
    """
    Removes a category contractor is available to transport
    Args:
        cargo_id: category's identifying number
        pool: a database connection
    Returns:
        True if successful, otherwise False
    """
    try:
        with pool.connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM cargo_capabilities WHERE id=%s;", (cargo_id,))
            connection.commit()
    except:
        return False
    return True


def db_get_cargo_owner(cargo_id: int, pool: ConnectionPool) -> bool:
    """
    Returns cargo owners contractor id number
    Args:
        cargo_id (int): cargos identifying number
        pool (ConnectionPool): a database connection
    Returns:
        contractor id, otherwise 0
    """
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT C.id FROM contractors C, contractor_locations CL, cargo_capabilities CC \
                WHERE C.id=CL.contractor_id AND CL.id=CC.contractor_location_id AND CC.id=%s;",
            (cargo_id,),
        )
        result = cursor.fetchone()[0]
    if not result:
        return 0
    return result


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
            (contractor_location_id,),
        )
        out = cursor.fetchall()
    if not out:
        return []
    return [CargoTypeInfo(*x[0:]) for x in out]

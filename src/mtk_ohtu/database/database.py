from psycopg_pool import ConnectionPool
from ..database.db_enums import CategoryType
from .db_datastructs import Listing, CargoTypeInfo, LogisticsNode
from ..logic.location import Location

# pylint: disable=E1129


def db_get_product_list(pool: ConnectionPool) -> list[Listing]:
    """Gets list of products from database
    Args:
        pool: a database connection pool
    Returns: list of Listings
    """
    out = None
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT l.id, l.category, l.price, l.address, l.description, u.username, l.longitude, l.latitude \
                        FROM listings as l \
                        LEFT JOIN users AS u ON u.id = l.user_id;"
        )
        out = [Listing(*x[0:6], Location((x[6], x[7]))) for x in cursor.fetchall()]
    return out


def db_get_product_by_id(product_id: int, pool: ConnectionPool) -> Listing | None:
    """Gets product from database by id
    Args:
        config: Database config
        product_id: Product id
    Returns:
        a Listing
        None if no product is found
    """
    out = None
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT l.category, l.price, l.address, l.description, u.username, l.longitude, l.latitude \
                        FROM listings as l \
                        LEFT JOIN users AS u ON u.id = l.user_id \
                        WHERE l.id=%s;",
            (product_id,),
        )
        out = cursor.fetchone()

    if out == None:
        return None

    l = Listing(product_id, *out[0:5], Location((out[5], out[6])))
    return l


def db_add_cargo_capability(
    cargo_id: int,
    cargo_type: CategoryType,
    price_per_hour: int,
    base_rate: int,
    max_capacity: int,
    max_distance: int,
    pool: ConnectionPool,
):
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
            "SELECT * FROM cargo_capabilities WHERE contractor_location_id=%s",
            (contractor_location_id,),
        )
        out = cursor.fetchall()
    if not out:
        return []
    return [CargoTypeInfo(*x[1:]) for x in out]


def db_get_logistics(pool: ConnectionPool) -> list[LogisticsNode]:
    """
    Gets all logistics contractor locations from database
    Args:
        pool: a database connection pool
    Returns: List of LogisticsNodes
    """
    out = None
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM contractor_locations AS c LEFT JOIN contractors AS s ON c.contractor_id=s.id"
        )
        out = [
            LogisticsNode(x[0], x[1], x[2], x[10], Location((x[5], x[6])), x[7])
            for x in cursor.fetchall()
        ]
    if not out:
        return None
    return out



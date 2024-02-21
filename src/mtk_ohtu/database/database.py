import psycopg
from ..database.db_enums import CategoryType
from psycopg_pool import ConnectionPool
from ..logic.listing import Listing
from ..logic.location import Location
from ..logic.logistics_node import LogisticsNode
from ..logic.cargo_type_info import CargoTypeInfo

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

    l = Listing(product_id, *out[0:5], Location((out[5], out[6])))
    return l


def db_get_user(username: str, pool: ConnectionPool) -> bool:
    """Gets user from database
    Args:
        config: Database config
        username: Username
        password: Password HASH
    Returns: True if user exists and password is correct, False otherwise
    """
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username=%s;", (username,))
        user = cursor.fetchone()
        if user:
            out = user
    return out


def db_check_if_user_exists():
    pass


def db_check_if_user_exists():
    pass


def db_add_user(
    username: str, password: str, email: str, pool: ConnectionPool
) -> tuple:
    """Adds user to database.
    Args:
        username: new username
        password: new password
        email: user email
        config: Database config
    Returns: (True, user id) if adding user succeeds, (False, None) if user already exists
    """
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        # "INSERT INTO users (username, password, email) VALUES (%s,%s,%s) RETURNING id",
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s,%s,%s) RETURNING id",
                (username, password, email),
            )
        except psycopg.errors.UniqueViolation:
            return (False, None)
        cursor.execute("SELECT id FROM users WHERE username=%s;", (username,))
        user = cursor.fetchone()
        out = (True, user[0])
    return out


def db_add_logistics(
    user_id: int,
    name: str,
    business_id: str,
    address: str,
    lon: float,
    lat: float,
    radius: int,
    pool: ConnectionPool,
):
    """
    Adds new logistics contractor to database
    Args:
        name: name of the logistics service provider
        business_id: business identification number (y-tunnus) if exists
        address: addres of the logistics service provider
        lon: longitude of the address
        lat: latitude of the address
        radius: how far is the contractor willing to deliver
        pool: database pool
    Returns:
        Returns the id of the new contractor
    """
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO logistics_contractors (user_id, name, business_id, address, longitude, latitude, delivery_radius) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id",
                (user_id, name, business_id, address, lon, lat, radius),
            )
            out = cursor.fetchone()[0]
        except psycopg.Error as e:
            print(f"Error inserting data: {e}")
    return out


def db_add_cargo_category(
    id: int,
    type: CategoryType,
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
            "INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate, max_capacity, max_distance) VALUES (%s,%s,%s,%s,%s,%s)",
            (id, type, price_per_hour, base_rate, max_capacity, max_distance),
        )
        out = True
    return out


def db_get_cargo_prices(logistic_id: int, pool: ConnectionPool) -> list[CargoTypeInfo]:
    """
    Gets contractor's prices for different cargo types

    Args:
        logistic_id: Contractor's id number

    Returns:
        a list of CargoTypeInfos
    """
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM cargo_prices WHERE logistic_id=%s", (logistic_id,)
        )
        out = cursor.fetchall()
    return [CargoTypeInfo(*x[1:]) for x in out]


def db_get_logistics(pool: ConnectionPool) -> list[LogisticsNode]:
    """
    Gets all logistics contractors from database
    Args:
        pool: a database connection pool
    Returns: List of LogisticsNodes
    """
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM logistics_contractors")
        out = [
            LogisticsNode(x[0], x[1], x[2], x[4], x[5], Location((x[6], x[7])), x[8])
            for x in cursor.fetchall()
        ]
    return out


def db_get_contractor(user_id: int, pool: ConnectionPool) -> LogisticsNode:
    """
    Gets logistics contractor information connected to user

    Args:
        user_id: Owner's user id number

    Returns:
        a LogisticsNode |
        None if no info is found
    """
    out = None
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM logistics_contractors WHERE user_id=%s", (user_id,)
        )
        out = cursor.fetchone()
    return LogisticsNode(*out[:3], out[4], out[5], Location((out[6], out[7])), out[8])

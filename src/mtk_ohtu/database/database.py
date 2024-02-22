import psycopg
from ..database.db_enums import CategoryType
from psycopg_pool import ConnectionPool
from ..logic.listing import Listing
from ..logic.location import Location
from ..logic.logistics_node import LogisticsNode
from ..logic.logistics_contractor import LogisticsContractor
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


def db_add_contractor(
    user_id: int,
    name: str,
    business_id: str,
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
                "INSERT INTO contractors (user_id, name, business_id) VALUES (%s,%s,%s) RETURNING id",
                (user_id, name, business_id),
            )
            out = cursor.fetchone()[0]
        except psycopg.Error as e:
            print(f"Error inserting data: {e}")
    return out

def db_add_contractor_location(
        contractor_id: int,
        address: str,
        telephone: str,
        email: str,
        longitude: float,
        latitude: float,
        radius: int,
        pool: ConnectionPool
):
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO contractor_locations (contractor_id, address, telephone, email, longitude, latitude, delivery_radius) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id",
                (contractor_id, address, telephone, email, longitude, latitude, radius),
            )
            out = cursor.fetchone()[0]
        except psycopg.Error as e:
            print(f"Error inserting data: {e}")
    return out

def db_add_cargo_capability(
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
            "INSERT INTO cargo_capabilities (contractor_location_id, type, price_per_km, base_rate, max_capacity, max_distance) VALUES (%s,%s,%s,%s,%s,%s)",
            (id, type, price_per_hour, base_rate, max_capacity, max_distance),
        )
        out = True
    return out


def db_get_location_cargo_capabilities(contractor_location_id: int, pool: ConnectionPool) -> list[CargoTypeInfo]:
    """
    Gets a list of sidestreams the location is available to deliver
    Args:
        contractor_location_id: location's identifying number
        pool: a database connection

    Returns:
        a list of CargoTypeInfos
        None if not available to deliver
    """
    out = None
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM cargo_capabilities WHERE contractor_location_id=%s", (contractor_location_id,)
        )
        out = cursor.fetchall()
    if not out:
        return None
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
        cursor.execute("SELECT * FROM contractor_locations AS c LEFT JOIN contractors AS s ON c.contractor_id=s.id")
        out = [
            LogisticsNode(x[0], x[1], x[2], x[10], Location((x[5], x[6])), x[7])
            for x in cursor.fetchall()
        ]
    if not out:
        return None
    return out


def db_get_contractor(user_id: int, pool: ConnectionPool) -> LogisticsContractor:
    """
    Gets contractor information connected to user

    Args:
        user_id: Owner's identifying number
        pool: a database connection

    Returns:
        a LogisticsContractor
        None if contractor doesnt't exist
    """
    out = None
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM contractors WHERE user_id=%s", (user_id,)
        )
        out = cursor.fetchone()
    if not out:
        return None
    return LogisticsContractor(out[0], out[1], out[2], out[4])

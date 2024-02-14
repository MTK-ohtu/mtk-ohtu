import psycopg
from database.db_enums import CategoryType
from psycopg_pool import ConnectionPool


# pylint: disable=E1129


def db_get_product_list(pool: ConnectionPool) -> list:
    """Gets list of products from database
    Args:
        config: Database config
    Returns: List of tuples, tuples in format ('product name', 'product price', 'product location', 'product description', 'seller name', longitude, latitude)
    """
    out = None
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT l.category, l.price, l.address, l.description, u.username, l.longitude, l.latitude, l.id \
                        FROM listings as l \
                        LEFT JOIN users AS u ON u.id = l.user_id;"
        )
        out = list(cursor.fetchall())
    return out


def db_get_product_by_id(product_id: int, pool: ConnectionPool) -> tuple:
    """Gets product from database by id
    Args:
        config: Database config
        product_id: Product id
    Returns: Tuple in format ('product name', 'product price', 'product location', 'product description', 'seller name', longitude, latitude)
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
    return out

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
        #"INSERT INTO users (username, password, email) VALUES (%s,%s,%s) RETURNING id",
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s,%s,%s) RETURNING id",
                (username, password, email)
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
    pool: ConnectionPool
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


def db_add_cargo_category(id: int, type: CategoryType, price_per_hour: int, base_rate: int, pool: ConnectionPool):
    """
    Adds new categories of materials that the contractor are capable to transport
    Args:
        id: id of the logistics contractor
        type: material type
        price_per_hour: price per hour for material transportation
        base_rate: base payment for material transportation
    """
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO cargo_prices (logistic_id, type, price_per_km, base_rate) VALUES (%s,%s,%s,%s)",
            (id, type, price_per_hour, base_rate)
        )
        out = True
    return out


def db_get_cargo_prices(logistic_id: int, pool: ConnectionPool):
    """
    Gets contractor's prices for different cargo types

    Args:
        logistic_id: Contractor's id number
    """
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM cargo_prices WHERE logistic_id=%s", (logistic_id,))
        out = cursor.fetchall()
    return out


def db_get_logistics(pool: ConnectionPool):
    """
    Gets all logistics contractors from database
    Args:
        config: Database config
    Returns: List of tuples, tuples in format ('name', 'business_id', 'address', 'longitude', 'latitude', 'delivery_radius')
    """
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM logistics_contractors")
        out = list(cursor.fetchall())
    return out


def db_get_contractors_by_euclidean(lat, lon, lat_r, lon_r, pool: ConnectionPool) -> list:
    """
    Queries all logistic contractors inside given euclidean distance from x,y
    Args:
        x: source longitude
        y: source latitude
        r: distance
        config: Database config
    """
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        query = f"SELECT longitude, latitude, name, address FROM logistics_contractors WHERE longitude BETWEEN {lon-lon_r} AND {lon+lon_r} AND latitude BETWEEN {lat-lat_r} AND {lat+lat_r}"
        cursor.execute(query)
        out = list(cursor.fetchall())
    return out


def db_get_contractor(user_id: int, pool: ConnectionPool):
    """
    Gets logistics contractor information connected to user

    Args:
        user_id: Owner's user id number
    """
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, business_id, address, delivery_radius FROM logistics_contractors WHERE user_id=%s", (user_id,))
        out = cursor.fetchone()
    return out
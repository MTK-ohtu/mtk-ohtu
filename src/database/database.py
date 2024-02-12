import psycopg
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


def db_get_user(username: str, password: str, pool: ConnectionPool) -> bool:
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
            out = user[1] == password
    return out


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
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email) (%s,%s,%s)",
                (username, password, email),
            )
        except psycopg.errors.UniqueViolation:
            return (False, None)
        cursor.execute("SELECT id FROM users WHERE username=%s;", (username,))
        user = cursor.fetchone()
        out = (True, user[0])
    return out


def db_add_logistics(
    name: str,
    business_id: str,
    address: str,
    vehicle_category: str,
    pool: ConnectionPool,
):
    """
    Adds new logistics service to database
    Args:
        name: name of the logistics service provider
        business_id: business identification number (y-tunnus) if exists
        address: addres of the logistics service provider
        vehicle_categories: types of equipment the provider has
        config: Database config
    Returns:
        True if data was inserted succesfully
    """
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO vehicles (logistic_id, name, vehicle_type, vehicle_capacity, price_per_hour) VALUES (%s,%s,%s,%s,%s)",
                (logistics_id, name, vehicle, max_weight, price),
            )
        except psycopg.Error as e:
            print(f"Error inserting data: {e}")
        out = True
    return out


def db_add_vehicle(vehicle: str, pool: ConnectionPool):
    pass


def db_get_logistics(pool: ConnectionPool):
    pass


def db_get_vehicle_categories(pool: ConnectionPool) -> list:
    """
    Gets vehicle categories from database
    Args:
        pool: Database connection pool
    Returns: Vehicle categories as a list"""
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT unnest(enum_range(NULL::vehichle_requirement_type))")
        out = [row[0] for row in cursor.fetchall()]
    return out


def db_get_material_categories(pool: ConnectionPool) -> list:
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT unnest(enum_range(NULL::category_type))")
        out = [row[0] for row in cursor.fetchall()]
    return out


def db_get_contractors_by_euclidean(x, y, r, pool: ConnectionPool) -> list:
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
        query = f"SELECT * FROM logistics_contractors WHERE x BETWEEN {x-r} AND {x+r} AND y BETWEEN {y-r} AND {y+r}"
        cursor.execute(query)
        out = list(cursor.fetchall())
    return out


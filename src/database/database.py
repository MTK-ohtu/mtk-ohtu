import psycopg
from database.db_meta import DatabaseConfig, db_connect

# pylint: disable=E1129

def db_get_product_list(config: DatabaseConfig) -> list:
    """Gets list of products from database
    Args:
        config: Database config
    Returns: List of tuples, tuples in format ('product name', 'product price', 'product location', 'product description', 'seller name', longitude, latitude)
    """
    connection = db_connect(config)
    out = None
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT l.category, l.price, l.address, l.description, u.username, l.longitude, l.latitude \
                        FROM listings as l \
                        LEFT JOIN users AS u ON u.id = l.user_id;"
        )
        out = list(cursor.fetchall())
    connection.close()
    return out


def db_get_user(username: str, password: str, config: DatabaseConfig) -> bool:
    """Gets user from database
    Args:
        config: Database config
        username: Username
        password: Password HASH
    Returns: True if user exists and password is correct, False otherwise
    """
    connection = db_connect(config)
    out = False
    with connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username=%s;", (username,))
        user = cursor.fetchone()
        if user:
            out = user[1] == password
    connection.close()
    return out


def db_add_user(
    username: str, password: str, email: str, config: DatabaseConfig
) -> tuple:
    """Adds user to database.
    Args:
        username: new username
        password: new password
        email: user email
        config: Database config
    Returns: (True, user id) if adding user succeeds, (False, None) if user already exists
    """
    connection = db_connect(config)
    out = False
    with connection:
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
    connection.close()
    return out


def db_add_logistics(
    name: str,
    business_id: str,
    address: str,
    config: DatabaseConfig
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
    connection = db_connect(config)
    logistics_id = None
    with connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO logistics_contractors (name, business_id, address) VALUES (%s,%s,%s) RETURNING id",
                (name, business_id, address),
            )
            logistics_id = cursor.fetchone()[0]
        except psycopg.Error as e:
            print(f"Error inserting data: {e}")
    connection.close()
    return logistics_id


def db_add_vehicle(logistics_id: int, name: str, vehicle: str, max_weight: int, price: int, config: DatabaseConfig):
    connection = db_connect(config)
    out = False
    with connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO vehicles (logistic_id, name, vehicle_type, vehicle_capacity, price_per_hour) VALUES (%s,%s,%s,%s,%s)",
                (logistics_id, name, vehicle, max_weight, price),
            )
        except psycopg.Error as e:
            print(f"Error inserting data: {e}")
        out = True
    connection.close()
    return out


def db_get_logistics(config: DatabaseConfig):
    pass


def db_get_vehicle_categories(config: DatabaseConfig) -> list:
    """
    Gets vehicle categories from database
    Args:
        config: Database config
    Returns: Vehicle categories as a list"""
    connection = db_connect(config)
    out = False
    with connection:
        cursor = connection.cursor()
        cursor.execute("SELECT unnest(enum_range(NULL::vehichle_requirement_type))")
        out = [row[0] for row in cursor.fetchall()]
    connection.close()
    return out

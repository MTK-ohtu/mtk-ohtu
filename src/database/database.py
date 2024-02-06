import psycopg2
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Object for storing database configuration information"""

    uri: str
    db_name: str
    user: str
    password: str
    port: int


def db_excecute_file(filename: str, config: DatabaseConfig):
    """Executes all commands in .sql file"""
    commands = ""
    with open(filename,"r") as f:
        commands = f.read()
    connection = db_connect(config)
    with connection:
        cursor = connection.cursor()
        cursor.execute(commands)
    connection.close()

def db_connect(config: DatabaseConfig):
    connection = psycopg2.connect(
        host=config.uri,
        database=config.db_name,
        user=config.user,
        password=config.password,
        port=config.port
    )
    return connection


def db_get_product_list(config: DatabaseConfig) -> list:
    """Gets list of products from database
    Args:
        config: Database config
    Returns: List of tuples, tuples in format ('product name', 'product price', 'product location', 'product description', 'seller name', (longitude, latitude))
    """
    connection = db_connect(config)
    out = None
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT l.category, l.price, l.address, l.description, u.username, l.coordinates \
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
        cursor.execute(
            "SELECT id, password FROM users WHERE username=%s;",
            (username,)
        )
        user = cursor.fetchone()
        if user:
            out = user[1] == password
    connection.close()
    return out

def db_add_user(username: str, password: str, email: str, config: DatabaseConfig) -> tuple:
    """Adds user to database.
    Args:
        username: new username
        password: new password
        email: user email
        config: Database config
    Returns: (True, user id) if adding user succeeds, (False, None) if user already exists"""
    connection = db_connect(config)
    out = False
    with connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email) (%s,%s,%s)",(username,password, email)
            )
        except psycopg2.errors.UniqueViolation:
            return (False, None)
        cursor.execute(
            "SELECT id FROM users WHERE username=%s;",
            (username,)
        )
        user = cursor.fetchone()
        out = (True, user[0])
    connection.close()
    return out

def add_logistics(config: DatabaseConfig):
    """Adds new logistics service to database"""
    pass

def db_get_logistics(config: DatabaseConfig):
    pass
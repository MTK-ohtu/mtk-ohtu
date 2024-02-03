import psycopg2
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Object for storing database configuration information"""

    uri: str
    db_name: str
    user: str
    password: str


def db_excecute_file(filename: str, config: DatabaseConfig):
    """Executes all commands in .sql file"""
    commands = ""
    with open(filename,"r") as f:
        commands = f.read()
        commands = [cmd.strip() for cmd in commands.split(";") if len(cmd)>0]
    connection = db_connect(config)
    with connection:
        cursor = connection.cursor()
        for cmd in commands:
            cursor.execute(cmd)
    connection.close()

def db_connect(config: DatabaseConfig):
    connection = psycopg2.connect(
        host=config.uri,
        database=config.db_name,
        user=config.user,
        password=config.password,
    )
    return connection


def db_get_product_list(config: DatabaseConfig) -> list:
    """Gets list of products from database
    Args:
        config: Database config
    Returns: List of tuples, tuples in format ('product name', 'product price', 'product location', 'product description', 'seller name')
    """
    connection = db_connect(config)
    out = None
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT p.name, p.price, p.location, p.description, s.name \
                        FROM products as p \
                        LEFT JOIN sellers AS s ON s.id = p.seller_id;"
        )
        out = list(cursor.fetchall())
    connection.close()
    return out

def db_get_user(username: str, password: str, config: DatabaseConfig) -> bool:
    """Gets user from database
    Args:
        config: Database config
        username: Username
        password: Password
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
import psycopg2
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Object for storing database configuration information"""

    uri: str
    db_name: str
    user: str
    password: str


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
    Returns: List of tuples, tuples in format ('product name', 'product price', 'product location', 'seller name')
    """
    connection = db_connect(config)
    out = None
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT p.name, p.price, p.location, s.name \
                        FROM products as p \
                        LEFT JOIN sellers AS s ON s.id == p.seller_id;"
        )
        out = list(cursor.fetchall())
    connection.close()
    return out

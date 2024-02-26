# pylint: disable=E1129


from mtk_ohtu.database.db_datastructs import Listing
from mtk_ohtu.logic.location import Location


from psycopg_pool import ConnectionPool


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
import psycopg
from psycopg_pool import ConnectionPool

from mtk_ohtu.database.db_datastructs import LogisticsContractor, LogisticsNode
from mtk_ohtu.logic.location import Location


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
    pool: ConnectionPool,
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


def db_get_contractor_locations(
    contractor_id: int, pool: ConnectionPool
) -> list[LogisticsNode]:
    """
    Gets contractors delivery locations

    Args:
        contractor_id: contractor's identifying number
        pool: a database connection

    Returns:
        List[LogisticsNode]: list of locations
    """
    out = []
    with pool.connection() as connection:
        cursor = connection.execute(
            "SELECT * FROM contractor_locations WHERE contractor_id=%s",
            (contractor_id,),
        )
        out = [
            LogisticsNode(x[0], x[1], x[2], None, Location((x[5], x[6])), x[7])
            for x in cursor.fetchall()
        ]
    if not out:
        return []
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
        cursor.execute("SELECT * FROM contractors WHERE user_id=%s", (user_id,))
        out = cursor.fetchone()
    if not out:
        return None
    return LogisticsContractor(out[0], out[1], out[2], out[4])


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
import psycopg
from psycopg_pool import ConnectionPool
from mtk_ohtu.database.db_datastructs import (
    LogisticsContractor,
    LogisticsNode,
    CategoryType,
    LocationService
)
from mtk_ohtu.logic.location import Location


# pylint: disable=E1129


def db_add_contractor(
    user_id: int,
    name: str,
    business_id: str,
    pool: ConnectionPool,
) -> bool:
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
    description: str,
    pool: ConnectionPool,
) -> bool:
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO contractor_locations (contractor_id, address, telephone, email, longitude, latitude, delivery_radius, description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id",
                (
                    contractor_id,
                    address,
                    telephone,
                    email,
                    longitude,
                    latitude,
                    radius,
                    description,
                ),
            )
            out = cursor.fetchone()[0]
        except psycopg.Error as e:
            print(f"Error inserting data: {e}")
    return out


def db_modify_contractor_location(
    location_id: int,
    address: str,
    telephone: str,
    email: str,
    longitude: float,
    latitude: float,
    radius: int,
    description: str,
    pool: ConnectionPool,
) -> bool:
    """
    Modifies the data of existing contractor location
    Args:
        location_id: locations identifying number
        address: location address
        telephone: telephone number
        email: email address
        longitude: coordinate
        latitude: coordinate
        radius: delivery radius
        description: location summary
        pool: a database connection

    Returns:
        bool: True if succesful, otherwise False
    """
    with pool.connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE contractor_locations SET address=%s, telephone=%s, email=%s, longitude=%s, latitude=%s, delivery_radius=%s, description=%s WHERE id=%s;",
                (
                    address,
                    telephone,
                    email,
                    longitude,
                    latitude,
                    radius,
                    description,
                    location_id,
                ),
            )
            connection.commit()
        except:
            return False
    return True


def db_remove_contractor_location(location_id: int, pool: ConnectionPool) -> bool:
    """
    Deletes contractor location
    Args:
        location_id: locations identifying number
        pool: a database connection
    Returns:
        bool: True if successful, otherwise False
    """
    with pool.connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "DELETE FROM contractor_locations WHERE id=%s;", (location_id,)
            )
            connection.commit()
        except:
            return False
    return True


def db_get_contractor_location_owner(location_id: int, pool: ConnectionPool) -> bool:
    """
    Returns location owners contractor id number
    Args:
        location_id: locations identifying number
        pool: a database connection
    Returns:
        contractor id, otherwise 0
    """
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT C.id FROM contractors C, contractor_locations CL WHERE CL.contractor_id=C.id AND CL.id=%s;",
            (location_id,),
        )
        result = cursor.fetchone()[0]
    if not result:
        return 0
    return result


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
            "SELECT * FROM contractor_locations WHERE contractor_id=%s;",
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
            "SELECT * FROM contractor_locations AS c LEFT JOIN contractors AS s ON c.contractor_id=s.id;"
        )
        out = [
            LogisticsNode(x[0], x[1], x[2], x[10], Location((x[5], x[6])), x[7])
            for x in cursor.fetchall()
        ]
    if not out:
        return None
    return out


def db_get_locations_by_cargo_type(
    category_type: CategoryType, pool: ConnectionPool
) -> list[LogisticsNode]:
    """
    Query all contractor locations capable of shipping given cargo type
    Args:
        type: type of cargo (enum CategoryType)
        pool: database connection
    """
    out = []
    with pool.connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT l.id, l.contractor_id, l.address, con.name, l.longitude, l.latitude, l.delivery_radius \
                FROM contractor_locations AS l \
                LEFT JOIN cargo_capabilities AS c \
                    ON l.id=c.contractor_location_id \
                LEFT JOIN contractors AS con ON l.contractor_id=con.id \
                WHERE c.category=%s;",
            (category_type.value,),
        )
        lista = cursor.fetchall()

        out = [
            LogisticsNode(x[0], x[1], x[2], x[3], Location((x[4], x[5])), x[6])
            for x in lista
        ]
    if not out:
        return []
    return out


def db_get_location_services_by_cargo_type(
        category_type: CategoryType, pool: ConnectionPool
) -> list[LocationService]:
    """
    Queries for location related information by given CategoryType.
    Returns collection (list) containing all information needed in front end.
    Args:
        category_type: type of cargo (enum CategoryType)
        pool: database connection
    Return: list[LocationService]    
    """
    out = []
    with pool.connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT l.contractor_id,\
                l.id,\
                con.name,\
                l.address,\
                l.telephone,\
                l.email,\
                l.longitude, l.latitude,\
                c.category,\
                c.price_per_km,\
                c.base_rate,\
                c.max_capacity,\
                c.max_distance,\
                l.delivery_radius,\
                c.unit,\
                c.can_process,\
                l.description \
                FROM contractor_locations AS l \
                LEFT JOIN cargo_capabilities AS c \
                    ON l.id=c.contractor_location_id \
                LEFT JOIN contractors AS con \
                    ON l.contractor_id=con.id \
                WHERE c.category=%s;",
            (category_type.value,),
        )
        lista = cursor.fetchall()
        for x in lista:
            print(x)
        out = [
            LocationService(x[0], x[1], x[2], x[3], x[4], x[5],
                            Location((x[6], x[7])), 
                            x[8].value, x[9], x[10],
                            x[11], x[12], x[13],
                            x[14].value, x[15], x[16])
            for x in lista
        ]
    if not out:
        return []
    return out

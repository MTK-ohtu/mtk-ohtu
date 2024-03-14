from datetime import datetime as dt
from psycopg import sql
from psycopg_pool import ConnectionPool
from ..database.db_datastructs import Listing, FullListing
from ..database.db_enums import SupplyDemandType, BatchUnitsType
from ..logic.location import Location


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

    if out == None:
        return None

    l = Listing(product_id, *out[0:5], Location((out[5], out[6])))
    return l


def db_create_new_listing_from_api_response(listing: FullListing, pool: ConnectionPool):
    """Creates (inserts) new listing from api object
    Args:
        listing: FullListing object
        pool: db pool
    Returns:
        True if successful
    """
    user_id = 1  # no uid in api, !!TEMP!!

    if listing.demand == SupplyDemandType.ONE_TIME:
        continuous = False
    else:
        continuous = True

    batch_size = 1  # Missing from API2 spec
    batch_type = BatchUnitsType.TN  # Missing from API2 spec, unknown solution

    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO listings \
                       (id, user_id, listing_type, category, subcategory, \
                       delivery_method, supply_demand, is_continuous, expiration_date, batch_size, batch_units, \
                       price, delivery_details, description, address, longitude, latitude, complies_with_regulations) \
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
            (
                listing.posting_id,
                user_id,
                listing.post_type,
                listing.category,
                listing.sub_category,
                listing.delivery_method,
                listing.demand,
                continuous,
                dt.fromtimestamp(listing.expiry_date),
                batch_size,
                batch_type,
                listing.price,
                listing.delivery_details,
                listing.description,
                listing.address,
                listing.location.longitude,
                listing.location.latitude,
                True,
            ),
        )
    return True


def db_update_listing_from_api_response(listing: FullListing, pool: ConnectionPool):
    """Updates listing from api object
    Args:
        listing: FullListing object
        pool: db pool
    Returns:
        True if successful
    """

    listings_dict = listing.update_dict()

    postid = listings_dict.pop("id")

    if "demand" in listings_dict:
        if listings_dict["demand"] == SupplyDemandType.ONE_TIME:
            listings_dict["continuous"] = False
        else:
            listings_dict["continuous"] = True
    if "location" in listings_dict:
        location = listings_dict.pop("location")
        listings_dict["longitude"] = location.longitude
        listings_dict["latitude"] = location.latitude

    update_column_compose = sql.SQL(',').join([sql.SQL('=').join([sql.Identifier(k), sql.Placeholder()]) for k in listings_dict])

    query = sql.SQL("UPDATE listings SET {columns} WHERE id = {postid};").format(
        columns=update_column_compose,
        postid=postid
    )

    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, list(listings_dict.values()))
    return True

def db_delete_listing_from_api_response(listing: FullListing, pool: ConnectionPool):
    """Updates listing from api object
    Args:
        listing: FullListing object
        pool: db pool
    Returns:
        True if successful
    """

    post_id = listing.posting_id

    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM listings WHERE id=%s CASCADE;", (post_id,))
    return True

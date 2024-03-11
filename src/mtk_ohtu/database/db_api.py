from .db_datastructs import APIKey
from psycopg_pool import ConnectionPool

def db_get_api_key(key: str, pool: ConnectionPool) -> APIKey | None:
    """Returns the API key with the provided string.

    Returns:
        An APIKey object
        None if the provided API key is invalid
    """

    with pool.connection() as connection:
        cur = connection.cursor()
        cur.execute("SELECT * FROM api_keys WHERE key = %s", (key,))
        found = cur.fetchone()

        if found is None:
            return None
        else:
            return APIKey(*found)
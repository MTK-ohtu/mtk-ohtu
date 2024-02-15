from os import getenv
from database.db_meta import (
    DatabaseConfig,
    db_create,
    db_connection_pool
)

SECRET_KEY = getenv("SECRET_KEY")
DATABASE_CONFIG = DatabaseConfig(
    uri=getenv("DATABASE_URL"),
    db_name=getenv("DATABASE_NAME"),
    user=getenv("DATABASE_USER"),
    password=getenv("DATABASE_PASSWORD"),
    port=getenv("DATABASE_PORT"),
)

NOMINATIM_DOMAIN = getenv("NOMINATIM_DOMAIN")
NOMINATIM_USER_AGENT = getenv("NOMINATIM_USER_AGENT")

def setup_db():
    db_create(DATABASE_CONFIG)
    return db_connection_pool(DATABASE_CONFIG)

DATABASE_POOL = setup_db()

# if SECRET_KEY in (None, "PUT_THE_KEY_HERE"):
#    raise Exception("Missing SECRET_KEY enviroment variable.")
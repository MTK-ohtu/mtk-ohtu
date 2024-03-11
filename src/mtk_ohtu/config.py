from os import getenv
from dotenv import load_dotenv, find_dotenv
from .database.db_meta import (
    DatabaseConfig,
    db_create,
    db_connection_pool,
    db_fake_connection_pool,
)

load_dotenv(find_dotenv(usecwd=True))

SECRET_KEY = getenv("SECRET_KEY")
DATABASE_CONFIG = DatabaseConfig(
    uri=getenv("DATABASE_URL"),
    db_name=getenv("DATABASE_NAME"),
    user=getenv("DATABASE_USER"),
    password=getenv("DATABASE_PASSWORD"),
    port=getenv("DATABASE_PORT"),
)
IS_TESTING = getenv("IS_TESTING")
NOMINATIM_DOMAIN = getenv("NOMINATIM_DOMAIN")
NOMINATIM_USER_AGENT = getenv("NOMINATIM_USER_AGENT")


def setup_db(testing=False):
    db_create(DATABASE_CONFIG)
    if testing:
        return db_fake_connection_pool(DATABASE_CONFIG)
    return db_connection_pool(DATABASE_CONFIG)


DATABASE_POOL = setup_db(testing=bool(IS_TESTING))

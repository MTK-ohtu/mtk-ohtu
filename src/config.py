from os import getenv
from database.database import DatabaseConfig

SECRET_KEY = getenv("SECRET_KEY")
DATABASE_CONFIG = DatabaseConfig(
    uri=getenv("DATABASE_URL"),
    db_name=getenv("DATABASE_NAME"),
    user=getenv("DATABASE_USER"),
    password=getenv("DATABASE_PASSWORD"),
    port=getenv("DATABASE_PORT")
)

# if SECRET_KEY in (None, "PUT_THE_KEY_HERE"):
#    raise Exception("Missing SECRET_KEY enviroment variable.")

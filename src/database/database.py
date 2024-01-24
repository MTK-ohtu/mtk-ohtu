import psycopg2
from os import getenv


def db_connect(uri: str, db_name: str, user: str, password: str):
    connection = psycopg2.connect(host=uri,
                            database=db_name,
                            user=user,
                            password=password)
    return connection


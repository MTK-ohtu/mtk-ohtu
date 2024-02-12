import psycopg
import database.db_enums as db_enums
from psycopg_pool import ConnectionPool
from dataclasses import dataclass
from psycopg.types.enum import EnumInfo, register_enum

# pylint: disable=E1129

@dataclass
class DatabaseConfig:
    """Object for storing database configuration information"""

    uri: str
    db_name: str
    user: str
    password: str
    port: int


def db_excecute_file(filename: str, config: DatabaseConfig):
    """Executes all commands in .sql file"""
    commands = ""
    with open(filename, "r") as f:
        commands = f.read()
    connection = db_connect(config)
    with connection:
        cursor = connection.cursor()
        cursor.execute(commands)
    connection.close()


def db_drop_all(config: DatabaseConfig):
    """UNSAFE; DO NOT EXPOSE! : Clear entire database"""
    connection = db_connect(config)
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            f"DROP SCHEMA public CASCADE; \
                        CREATE SCHEMA public; \
                        GRANT ALL ON SCHEMA public TO {config.user}; \
                        GRANT ALL ON SCHEMA public TO public;"
        )

    connection.close()

def _db_connection_string(config: DatabaseConfig) -> str:
    conn_args_dict = {'host': config.uri,
        'dbname': config.db_name,
        'user': config.user,
        'password': config.password,
        'port': config.port}
    
    conn_args = [(k,conn_args_dict[k]) for k in conn_args_dict if conn_args_dict[k]]
    conn_args = " ".join([f"{k}={v}" for k,v in conn_args])
    return conn_args


def db_connection_pool(config: DatabaseConfig) -> ConnectionPool:
    conn_args = _db_connection_string(config)

    connection_pool = ConnectionPool(
        conninfo=conn_args,
        min_size=1,
        max_size=5,
        configure=db_register_enums
    )
    return connection_pool


def db_connect(config: DatabaseConfig) -> psycopg.Connection:
    conn_args = _db_connection_string(config)

    connection = psycopg.connect(conn_args)
    return connection


def db_create(config: DatabaseConfig):
    """Creates database and python mappings for enums"""
    db_excecute_file("schema.sql", config)

def db_register_enums(connection):
    for enm in db_enums.DEFINED_ENUMS:
        enum_object = db_enums.DEFINED_ENUMS[enm]
        register_enum(EnumInfo.fetch(connection, enm), connection, enum_object, mapping={m: m.value for m in enum_object})

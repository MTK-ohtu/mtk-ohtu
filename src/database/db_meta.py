import psycopg
from dataclasses import dataclass


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


def db_connect(config: DatabaseConfig) -> psycopg.Connection:
    conn_args_dict = {'host': config.uri,
        'dbname': config.db_name,
        'user': config.user,
        'password': config.password,
        'port': config.port}
    
    conn_args = [(k,conn_args_dict[k]) for k in conn_args_dict if conn_args_dict[k]]
    conn_args = " ".join([f"{k}={v}" for k,v in conn_args])
    
    connection = psycopg.connect(conn_args)
    return connection


def db_create(config: DatabaseConfig):
    """Creates database and python mappings for enums"""
    db_excecute_file("schema.sql")

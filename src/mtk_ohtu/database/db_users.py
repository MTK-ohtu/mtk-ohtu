import psycopg
from psycopg_pool import ConnectionPool

# pylint: disable=E1129

def db_get_user(username: str, pool: ConnectionPool) -> bool:
    """Gets user from database
    Args:
        config: Database config
        username: Username
        password: Password HASH
    Returns: True if user exists and password is correct, False otherwise
    """
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username=%s;", (username,))
        user = cursor.fetchone()
        if user:
            out = user
    return out


def db_check_if_user_exists():
    pass


def db_add_user(
    username: str, password: str, email: str, pool: ConnectionPool
) -> tuple:
    """Adds user to database.
    Args:
        username: new username
        password: new password
        email: user email
        config: Database config
    Returns: (True, user id) if adding user succeeds, (False, None) if user already exists
    """
    out = False
    with pool.connection() as connection:
        cursor = connection.cursor()
        # "INSERT INTO users (username, password, email) VALUES (%s,%s,%s) RETURNING id",
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s,%s,%s) RETURNING id",
                (username, password, email),
            )
        except psycopg.errors.UniqueViolation:
            return (False, None)
        cursor.execute("SELECT id FROM users WHERE username=%s;", (username,))
        user = cursor.fetchone()
        out = (True, user[0])
    return out

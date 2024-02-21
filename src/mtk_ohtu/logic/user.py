from ..database import database as db
from flask import session
import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from ..config import DATABASE_POOL


def register(username, password, email):
    hash_value = generate_password_hash(password)

    db.db_add_user(username, hash_value, email, DATABASE_POOL)

    return login(username, password)


def login(username, password):
    """
    Logs in a user with the given username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        bool: True if the login is successful, False otherwise.
    """

    user = db.db_get_user(username, DATABASE_POOL)
    if not user:
        return False
    elif user and check_password_hash(user[1], password):
        session["user_id"] = user[0]
        session["csrf_token"] = secrets.token_hex(16)

        contractor = db.db_get_contractor(user[0], DATABASE_POOL)
        if contractor:
           session["contractor_id"] = contractor.id
        return True


def logout():
    del session["user_id"]
    session.pop("contractor_id", None)


def user_id():
    return session.get("user_id", 0)

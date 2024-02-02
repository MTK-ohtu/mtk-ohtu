from src import database as db
from flask import session
import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from config import DATABASE_CONFIG



"""
def register(username, password):
    hash_value = generate_password_hash(password)

    sql = "INSERT INTO users (username,password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()

    return login(username, password)
"""

def login(username, password):
    """
    Logs in a user with the given username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        bool: True if the login is successful, False otherwise.
    """

    user = db.get_user(username, password, DATABASE_CONFIG)
    if user:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["csrf_token"] = secrets.token_hex(16)
            return True
    else:
        return False


def logout():
    del session["user_id"]

def user_id():
    return session["user_id",0]
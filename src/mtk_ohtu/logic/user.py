import secrets
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import mtk_ohtu.database.db_users
from ..database import db_contractors as db
from ..config import DATABASE_POOL


"""class LoginForm(Form):
    username = StringField("Username", [validators.Length(min=4, max=25)])
    password = PasswordField("Password", [validators.Length(min=4, max=25)])"""
   

def register(username, password, email):
    hash_value = generate_password_hash(password)

    if username == "" or password == "" or email == "":
        return False

    #check if username is already in use
    if mtk_ohtu.database.db_users.db_get_user(username, DATABASE_POOL):
        return False


    mtk_ohtu.database.db_users.db_add_user(username, hash_value, email, DATABASE_POOL)

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

    user = mtk_ohtu.database.db_users.db_get_user(username, DATABASE_POOL)
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
    try:
        del session["user_id"]
        session.pop("contractor_id", None)
    except KeyError:
        pass


def user_id():
    return session.get("user_id", 0)

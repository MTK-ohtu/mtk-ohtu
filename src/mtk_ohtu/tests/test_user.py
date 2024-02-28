import pytest
from flask import session
from mtk_ohtu.logic import user as u


def test_register_with_new_email(app):
    with app.test_request_context():
        response = u.register("new_test_user", "New test password", "new_email")
        assert response is True

def test_register_with_existing_username(app):
    with app.test_request_context():
        u.register("new_test_user", "New test password", "new_email")

        response = u.register("new_test_user", "New test password", "new_email")
        assert response is False

def test_login_with_valid_credentials(app):
    with app.test_request_context():
        u.register("cool_test_user", "Cool test password", "random")    
        response = u.login("cool_test_user", "Cool test password")
        assert response is True

def test_login_with_invalid_credentials(app):
    with app.test_request_context():
        response = u.login("cool_test_user", "Wrong password")
        assert response is False
        assert session.get("username") is None

def test_logout(app):
    with app.test_request_context():
        u.login("cool_test_user", "Cool test password")
        u.logout()
        assert session.get("username") is None


import pytest
import unittest
from flask import session
from mtk_ohtu import app as mtkapp
from mtk_ohtu.database import db_meta as dbm
from mtk_ohtu.config import DATABASE_CONFIG

@pytest.fixture()
def app():
    app = mtkapp.create_app()
    app.config.update({
        "TESTING": True,
    })
    dbm.db_drop_all(DATABASE_CONFIG)
    dbm.db_create(DATABASE_CONFIG)
    dbm.db_excecute_file("db_mock_data.sql", DATABASE_CONFIG)

    yield app

    dbm.db_drop_all(DATABASE_CONFIG)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_index(client):
    response = client.get("/")
    assert b"<h1>Welcome to the MTK - OhTU project page</h1>" in response.data


# user route tests
    
def test_login_as_test_user(client):
    with client:
        response = client.post("/login", data={
            "username": "testuser",
            "password": "testpassword"}, follow_redirects=True)
        assert session["user_id"] == 9
        assert response.request.path == "/"

def test_login_fails_with_wrong_password(client):
    with client:
        response = client.post("/login", data={
            "username": "testuser",
            "password": "wrong"})
        
        with pytest.raises(KeyError):
            session["user_id"]
        assert "Salasana tai käyttäjätunnus väärin".encode('utf8') in response.data

def test_login_fails_when_user_not_exists(client):
    with client:
        response = client.post("/login", data={
            "username": "wronguser",
            "password": "wrong"})
        
        with pytest.raises(KeyError):
            session["user_id"]
        assert "Salasana tai käyttäjätunnus väärin".encode('utf8') in response.data


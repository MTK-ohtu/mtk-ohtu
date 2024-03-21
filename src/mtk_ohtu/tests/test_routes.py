import pytest
import logging
from flask import session


def post_test(client, route, data):
    return client.post('/fi'+ route, follow_redirects=True, headers={'Accept-Language': 'fi'}, data=data)

def get_test(client, route):
    return client.get(route, follow_redirects=True, headers={'Accept-Language': 'fi'})

def test_index(client):
    with client:
        response = get_test(client, "/")
        assert b"<h1>MTK-Ohtu</h1>" in response.data


# user route tests


def test_login_as_test_user(client):
    with client:
        response = post_test(client, 
            "/login",
            data={"username": "testuser", "password": "testpassword"},
        )
        logging.warning(session)
        assert session["user_id"] == 9
        assert response.request.path == "/fi/"


def test_login_fails_with_wrong_password(client):
    with client:
        response = post_test(client,
            "/login", data={"username": "testuser", "password": "wrong"}
        )

        with pytest.raises(KeyError):
            session["user_id"]
        assert "Salasana tai käyttäjätunnus väärin".encode("utf8") in response.data


def test_login_fails_when_user_not_exists(client):
    with client:
        response = post_test(client,
            "/login", data={"username": "wronguser", "password": "wrong"}
        )

        with pytest.raises(KeyError):
            session["user_id"]
        assert "Salasana tai käyttäjätunnus väärin".encode("utf8") in response.data


def test_logout_clears_user_id_from_session(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 9

    with client:
        response = get_test(client, "/logout")
        with pytest.raises(KeyError):
            session["user_id"]
        assert response.request.path == "/fi/"


def test_logout_without_login(client):
    with client:
        response = get_test(client, "/logout")
        with pytest.raises(KeyError):
            session["user_id"]
        assert response.request.path == "/fi/"


def test_register(client):
    with client:
        response = post_test(client,
            "/register",
            data={
                "username": "cool_test_user",
                "password": "Cool test password",
                "email": "a@a.com",
            }
        )

        assert "user_id" in session
        assert response.request.path == "/fi/"


def test_contractor_redirect(client):
    with client:
        response = get_test(client, "/contractor")
        assert response.request.path == "/fi/addlogistics"


def test_contractor_listing(client):
    with client:
        post_test(client,
            "/login", data={"username": "testikayttaja1", "password": "testpassword"}
        )

        response = get_test(client, "/contractor")
        assert b"Urpunistintie 8" in response.data
        assert b"500" in response.data
        assert b"Saaninranta" in response.data

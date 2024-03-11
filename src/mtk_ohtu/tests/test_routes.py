import pytest
from flask import session


def test_index(client):
    response = client.get("/")
    assert b"<h1>Welcome to the MTK - OhTU project page</h1>" in response.data


# user route tests


def test_login_as_test_user(client):
    with client:
        response = client.post(
            "/login",
            data={"username": "testuser", "password": "testpassword"},
            follow_redirects=True,
        )
        assert session["user_id"] == 9
        assert response.request.path == "/"


def test_login_fails_with_wrong_password(client):
    with client:
        response = client.post(
            "/login", data={"username": "testuser", "password": "wrong"}
        )

        with pytest.raises(KeyError):
            session["user_id"]
        assert "Salasana tai käyttäjätunnus väärin".encode("utf8") in response.data


def test_login_fails_when_user_not_exists(client):
    with client:
        response = client.post(
            "/login", data={"username": "wronguser", "password": "wrong"}
        )

        with pytest.raises(KeyError):
            session["user_id"]
        assert "Salasana tai käyttäjätunnus väärin".encode("utf8") in response.data


def test_logout_clears_user_id_from_session(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 9

    with client:
        response = client.get("/logout", follow_redirects=True)
        with pytest.raises(KeyError):
            session["user_id"]
        assert response.request.path == "/"


def test_logout_without_login(client):
    with client:
        response = client.get("/logout", follow_redirects=True)
        with pytest.raises(KeyError):
            session["user_id"]
        assert response.request.path == "/"


def test_register(client):
    with client:
        response = client.post(
            "/register",
            data={
                "username": "cool_test_user",
                "password": "Cool test password",
                "email": "a@a.com",
            },
            follow_redirects=True,
        )

        assert "user_id" in session
        assert response.request.path == "/"


def test_contractor_redirect(client):
    with client:
        response = client.get("/contractor", follow_redirects=True)
        assert response.request.path == "/addlogistics"


def test_contractor_listing(client):
    with client:
        client.post(
            "/login", data={"username": "testikayttaja1", "password": "testpassword"}
        )

        response = client.get("/contractor")
        assert b"Urpunistintie 8" in response.data
        assert b"500" in response.data
        assert b"Saaninranta" in response.data

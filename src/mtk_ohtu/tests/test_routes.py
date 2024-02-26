import pytest
from flask import session


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


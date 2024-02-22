import pytest
import unittest
from mtk_ohtu import app as mtkapp
from mtk_ohtu.database import db_meta as dbm
from mtk_ohtu.config import DATABASE_CONFIG

@pytest.fixture()
def app():
    app = mtkapp.create_app()
    app.config.update({
        "TESTING": True,
    })

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


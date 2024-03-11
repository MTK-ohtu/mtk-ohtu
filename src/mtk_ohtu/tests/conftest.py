import pytest
from mtk_ohtu import app as mtkapp
from mtk_ohtu.database import db_meta as dbm
import mtk_ohtu.config as config


# Database testing fixtures

@pytest.fixture()
def datapool():
    dbm.db_excecute_file("schema.sql", config.DATABASE_CONFIG)
    dbm.db_excecute_file("db_mock_data.sql", config.DATABASE_CONFIG)
    pool = dbm.db_connection_pool(config.DATABASE_CONFIG)
    yield pool
    pool.close()
    dbm.db_drop_all(config.DATABASE_CONFIG)

# Route testing fixtures

@pytest.fixture()
def app():
    app = mtkapp.create_app()
    app.config['WTF_CSRF_ENABLED']=False
    app.config.update(
        {
            "TESTING": True,
        }
    )
    dbm.db_drop_all(config.DATABASE_CONFIG)
    dbm.db_create(config.DATABASE_CONFIG)
    dbm.db_excecute_file("db_mock_data.sql", config.DATABASE_CONFIG)
    yield app
    dbm.db_drop_all(config.DATABASE_CONFIG)


@pytest.fixture()
def client(app):
    yield app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

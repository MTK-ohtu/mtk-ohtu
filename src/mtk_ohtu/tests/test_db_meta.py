import unittest
from psycopg import ProgrammingError
import mtk_ohtu.database.db_meta as db_m
from mtk_ohtu.config import DATABASE_CONFIG


class TestConnectionAndCreation(unittest.TestCase):
    def test_config_exists(self):
        db_conf = DATABASE_CONFIG
        self.assertTrue(len(db_conf.uri) > 0)
        self.assertTrue(len(db_conf.user) > 0)
        self.assertTrue(len(db_conf.password) > 0)
        self.assertTrue(len(db_conf.db_name) > 0)
        self.assertTrue(len(db_conf.port) > 0)

    def test_connection_function_works(self):
        connection = db_m.db_connect(DATABASE_CONFIG)
        connection.close()
        self.assertTrue(True)

    def test_database_schema_creation_mock_data_and_removal_works(self):
        db_m.db_drop_all(DATABASE_CONFIG)
        db_m.db_excecute_file("schema.sql", DATABASE_CONFIG)
        connection = db_m.db_connect(DATABASE_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM listings LIMIT 1;")
        connection.close()
        self.assertTrue(True)

        db_m.db_excecute_file("db_mock_data.sql", DATABASE_CONFIG)
        connection = db_m.db_connect(DATABASE_CONFIG)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT complies_with_regulations FROM listings WHERE delivery_method = 'pickup' LIMIT 1;"
        )
        self.assertTrue(cursor.fetchone()[0])
        connection.close()

        db_m.db_drop_all(DATABASE_CONFIG)
        connection = db_m.db_connect(DATABASE_CONFIG)
        cursor = connection.cursor()
        success = False
        try:
            cursor.execute("SELECT id FROM listings LIMIT 1;")
        except ProgrammingError:
            success = True
        self.assertTrue(success)
        connection.close()

import unittest
import database.database as db
from config import DATABASE_CONFIG
from psycopg2 import ProgrammingError

class TestConnectionAndCreation(unittest.TestCase):
    def test_config_exists(self):
        db_conf = DATABASE_CONFIG
        self.assertTrue(len(db_conf.uri) > 0)
        self.assertTrue(len(db_conf.user) > 0)
        self.assertTrue(len(db_conf.password) > 0)
        self.assertTrue(len(db_conf.db_name) > 0)
        self.assertTrue(len(db_conf.port) > 0)

    def test_connection_function_works(self):
        connection = db.db_connect(DATABASE_CONFIG)
        connection.close()
        self.assertTrue(True)
    
    def test_database_schema_creation_mock_data_and_removal_works(self):
        db.db_excecute_file('schema.sql', DATABASE_CONFIG)
        connection = db.db_connect(DATABASE_CONFIG)
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM listings LIMIT 1;')
        connection.close()
        self.assertTrue(True)

        db.db_excecute_file('db_mock_data.sql', DATABASE_CONFIG)
        connection = db.db_connect(DATABASE_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT complies_with_regulations FROM listings WHERE delivery_method = 'pickup' LIMIT 1;")
        self.assertTrue(cursor.fetchone()[0])
        connection.close()

        db.db_drop_all(DATABASE_CONFIG)
        connection = db.db_connect(DATABASE_CONFIG)
        cursor = connection.cursor()
        success = False
        try:
            cursor.execute('SELECT id FROM listings LIMIT 1;')
        except ProgrammingError:
            success = True
        self.assertTrue(success)
        connection.close()
        

class TestSelecions(unittest.TestCase):
    def setUp(self):
        db.db_excecute_file('schema.sql', DATABASE_CONFIG)
        db.db_excecute_file('db_mock_data.sql', DATABASE_CONFIG)

    def test_todo(self):
        self.assertTrue(True)

    def tearDown(self):
        db.db_drop_all(DATABASE_CONFIG)

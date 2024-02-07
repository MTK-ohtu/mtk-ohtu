import unittest
import database.database as db
from config import DATABASE_CONFIG

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

class TestSelecions(unittest.TestCase):
    def test_todo(self):
        self.assertTrue(True)

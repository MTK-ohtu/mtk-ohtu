import unittest
import mtk_ohtu.logic.logistics as l
import mtk_ohtu.database.db_meta as db_m
from mtk_ohtu.config import DATABASE_CONFIG

class TestLogistics(unittest.TestCase):
    def setUp(self):
        db_m.db_excecute_file("schema.sql", DATABASE_CONFIG)
        db_m.db_excecute_file("db_mock_data.sql", DATABASE_CONFIG)
        self.pool = db_m.db_connection_pool(DATABASE_CONFIG)

        self.userid = 1
        self.name  = "rekka oy"
        self.business = "1234567-1"
        self.address = "Simonkatu 6"
        self.radius = 200
        self.categories = ['Manure']
        self.base_rates = ['200']
        self.prices_per_hour = ['15']
        self.max_capacities = ['50']
        self.max_distances = ['300']

    def test_addlogistics_returns_false_when_address_not_found(self):
        self.address = "aaaaaaaaaaaaaaaaaaaaa"
        result = l.addlogistics(
            self.userid, 
            self.name, 
            self.business, 
            self.address, 
            self.radius, 
            self.categories, 
            self.base_rates,
            self.prices_per_hour,
            self.max_capacities,
            self.max_distances
        )
        self.assertFalse(result)

    def test_addlogistics_returns_true_when_data_is_correct(self):
        result = l.addlogistics(
            self.userid, 
            self.name, 
            self.business, 
            self.address, 
            self.radius, 
            self.categories, 
            self.base_rates,
            self.prices_per_hour,
            self.max_capacities,
            self.max_distances
        )
        self.assertTrue(result)

    def tearDown(self):
        self.pool.close()
        db_m.db_drop_all(DATABASE_CONFIG)
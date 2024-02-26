import unittest
import mtk_ohtu.logic.logistics as l
import mtk_ohtu.database.db_meta as db_m
from mtk_ohtu.config import DATABASE_CONFIG


class TestLogistics(unittest.TestCase):
    def setUp(self):
        db_m.db_excecute_file("schema.sql", DATABASE_CONFIG)
        db_m.db_excecute_file("db_mock_data.sql", DATABASE_CONFIG)
        self.pool = db_m.db_connection_pool(DATABASE_CONFIG)

        self.user_id = 1
        self.contractor_id = 1
        self.contractor_location_id = 1
        self.name = "rekka oy"
        self.business = "1234567-1"
        self.address = "Simonkatu 6"
        self.postcode = "00100"
        self.city = "Helsinki"
        self.email = "rekka@gmail.com"
        self.phone = "040-1234567"
        self.radius = 200
        self.categories = ["Manure"]
        self.base_rates = ["200"]
        self.prices_per_hour = ["15"]
        self.max_capacities = ["50"]
        self.max_distances = ["300"]

    def test_add_contractor(self):
        result = l.add_contractor(self.user_id, self.name, self.business)
        self.assertTrue(result)

    def test_add_contractor_location(self):
        result = l.add_contractor_location(
            self.contractor_id,
            self.address,
            self.postcode,
            self.city,
            self.phone,
            self.email,
            self.radius
        )
        self.assertTrue(result)

    def test_add_cargo_capability(self):
        result = l.add_cargo_capability(
            self.contractor_location_id,
            self.categories,
            self.base_rates,
            self.prices_per_hour,
            self.max_capacities,
            self.max_distances,
        )
        self.assertTrue(result)

    def test_add_contractor_location_returns_false_when_address_not_found(self):
        self.address = "aaaaaaaaaaaaaaaaaaaaa"
        result = l.add_contractor_location(
            self.contractor_id,
            self.address,
            self.postcode,
            self.city,
            self.phone,
            self.email,
            self.radius
        )
        self.assertFalse(result)

    def tearDown(self):
        self.pool.close()
        db_m.db_drop_all(DATABASE_CONFIG)

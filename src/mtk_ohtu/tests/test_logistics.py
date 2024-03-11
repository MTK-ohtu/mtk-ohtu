import unittest
import mtk_ohtu.logic.logistics as l
import mtk_ohtu.database.db_meta as db_m
from mtk_ohtu.logic import user as u
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
        self.radius = -1
        self.description = "test"

        self.category = "Dry manure"
        self.base_rate = 200
        self.price_per_hour = 15
        self.max_capacity = 50
        self.max_distance = 300
        self.unit = "tn"
        self.can_process = True

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
            self.radius,
            self.description,
        )
        self.assertTrue(result)

    def test_add_cargo_capability(self):
        result = l.add_cargo_capability(
            self.contractor_location_id,
            self.category,
            self.base_rate,
            self.price_per_hour,
            self.max_capacity,
            self.max_distance,
            self.unit,
            self.can_process,
            self.description,
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
            self.radius,
            self.description,
        )
        self.assertFalse(result)

    def test_cargo_capability_with_empty_inputs(self):
        self.base_rate = ""
        self.price_per_hour = ""
        self.max_capacity = ""
        result = l.add_cargo_capability(
            self.contractor_location_id,
            self.category,
            self.base_rate,
            self.price_per_hour,
            self.max_capacity,
            self.max_distance,
            self.unit,
            self.can_process,
            self.description,
        )
        self.assertTrue(result)

    def test_contractor_locations_returns_correct_amount_of_locations(self):
        result = l.contractor_locations(self.contractor_id)
        self.assertEqual(len(result), 3)

    def test_contractor_locations_returns_empty_list_if_none_exists(self):
        contractor_id = 8
        result = l.contractor_locations(contractor_id)
        self.assertEqual(len(result), 0)

    def test_cargo_capability_returns_correct_amount_of_capabilities(self):
        result = l.cargo_capability(self.contractor_location_id)
        self.assertEqual(len(result), 3)

        contractor_location_id = 3
        result = l.cargo_capability(contractor_location_id)
        self.assertEqual(len(result), 4)

    def test_cargo_capability_returns_empty_list_if_none_is_set(self):
        # No cargo capabilities added to contractor_location_id 10 in test data
        contractor_location_id = 10
        result = l.cargo_capability(contractor_location_id)
        self.assertEqual(len(result), 0)

    def test_get_locations_and_cargo_capability_returns_correct_amount_of_locations_and_capabilities(
        self,
    ):
        # 3 locations with 3, 3 and 4 capabilities
        result = l.get_locations_and_cargo_capability(self.contractor_id)
        self.assertEqual(len(result), 3)

        loc1 = result[0][1]
        loc2 = result[1][1]
        loc3 = result[2][1]
        self.assertEqual(len(loc1), 3)
        self.assertEqual(len(loc2), 3)
        self.assertEqual(len(loc3), 4)

    def test_modify_contractor_location_returns_true_when_updating_succeeds(self):
        result = l.modify_contractor_location(
            self.contractor_location_id,
            "A.I: Virtasen aukio",
            "00550",
            "Helsinki",
            "0400000000",
            "testi@gmail.com",
            "200",
            "-"
        )
        self.assertTrue(result)

    def test_modify_contractor_location_returns_false_with_nonexistent_address(self):
        result = l.modify_contractor_location(
            self.contractor_location_id,
            "xxxxx",
            "0000",
            "Helsinki",
            "0400000000",
            "testi@gmail.com",
            "200",
            "-"
        )
        self.assertFalse(result)

    def test_remove_contractor_location_returns_true_when_successful(self):
        result = l.remove_contractor_location(self.contractor_location_id)
        self.assertTrue(result)

    def test_check_asset_ownership_returns_true_when_contractor_is_owner(self):
        cargo_result = l.check_asset_ownership("cargo", 8, 1)
        location_result = l.check_asset_ownership("location", 9, 6)
        self.assertTrue(cargo_result)
        self.assertTrue(location_result)

    def test_check_asset_ownership_returns_false_when_contractor_isnt_owner(self):
        cargo_result = l.check_asset_ownership("cargo", 10, 2)
        location_result = l.check_asset_ownership("location", 8, 2)
        self.assertFalse(cargo_result)
        self.assertFalse(location_result)

    def test_check_asset_ownership_returns_false_with_unrecognized_type(self):
        result = l.check_asset_ownership("test-type", 10, 2)
        self.assertFalse(result)

    def tearDown(self):
        self.pool.close()
        db_m.db_drop_all(DATABASE_CONFIG)

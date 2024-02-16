import unittest
import logic.logistics as l

class TestLogistics(unittest.TestCase):
    def setUp(self):
        self.type = "private"
        self.userid = 1
        self.name  = "rekka oy"
        self.business = None
        self.address = "Simonkatu 6"
        self.radius = 200
        self.categories = ['Manure']
        self.base_rates = ['200']
        self.prices_per_hour = ['15']

    def test_addlogistics_returns_false_when_address_not_found(self):
        self.address = "aaaaaaaaaaaaaaaaaaaaa"
        result = l.addlogistics(
            self.type, 
            self.userid, 
            self.name, 
            self.business, 
            self.address, 
            self.radius, 
            self.categories, 
            self.base_rates,
            self.prices_per_hour
        )
        self.assertFalse(result)

    def test_addlogistics_returns_true_when_data_is_correct(self):
        result = l.addlogistics(
            self.type, 
            self.userid, 
            self.name, 
            self.business, 
            self.address, 
            self.radius, 
            self.categories, 
            self.base_rates,
            self.prices_per_hour
        )
        self.assertTrue(result)
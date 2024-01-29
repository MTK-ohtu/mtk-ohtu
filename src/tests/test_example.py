import unittest
from logic.route_calculator import Route


class TestRoute(unittest.TestCase):
    def setUp(self):
        self.loc1 = "Gustaf Hällströmin katu 2, 00560 Helsinki"
        self.loc2 = "Leppäsuonkatu 11"
        self.email = "miko.paajanen@helsinki.fi"

        self.demo_route = Route(self.loc1, self.loc2, self.email)

    def test_check_distance_correct(self):
        self.assertEqual(self.demo_route.distance, 5441.6)

    def test_check_duration_correct(self):
        self.assertEqual(self.demo_route.duration, 1056.3)

    #def test_geo_correct(self):
    #    self.assertAlmostEqual(self.demo_route.geodesic_distance(), 4567.9, places=1)

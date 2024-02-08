import unittest
from logic.route_calculator import Route
from logic.location import Location


class TestRoute(unittest.TestCase):
    def setUp(self):
        self.loc1 = Location((24.962548,60.205298))
        self.loc2 = Location((24.922388,60.169232))
        self.email = "miko.paajanen@helsinki.fi"

        self.demo_route = Route(self.loc1, self.loc2)
        self.demo_route.calculate_route()

    def test_check_distance_correct(self):
        result = False
        if 5500 < self.demo_route.distance < 5600:
            result = True
        self.assertTrue(result)

    def test_check_duration_correct(self):
        result = False
        if 1050 < self.demo_route.duration < 1100:
            result = True
        self.assertTrue(result)

    # def test_geo_correct(self):
    #    self.assertAlmostEqual(self.demo_route.geodesic_distance(), 4567.9, places=1)

import unittest
from unittest.mock import patch, MagicMock
from mtk_ohtu.logic.route_calculator import Route
from mtk_ohtu.logic.location import Location


class TestRoute(unittest.TestCase):
    @patch("mtk_ohtu.logic.location.Location")  # Mock the Location class
    def setUp(self, mock_location_class):
        # Create separate mock instances for each location
        location1_mock = MagicMock()
        location1_mock.latitude = 60.205298
        location1_mock.longitude = 24.962548

        location2_mock = MagicMock()
        location2_mock.latitude = 60.169232
        location2_mock.longitude = 24.922388

        # Use side_effect to return different mocks for consecutive calls
        mock_location_class.side_effect = [location1_mock, location2_mock]

        self.location1 = mock_location_class()
        self.location2 = mock_location_class()

        self.api_key = "test_api_key"
        self.route = Route(self.location1, self.location2, self.api_key)

    def test_init(self):
        # Test initialization and attribute assignments
        self.assertEqual(self.route.location1, self.location1)
        self.assertEqual(self.route.location2, self.location2)
        self.assertEqual(self.route.api_key, self.api_key)
        self.assertEqual(self.route.distance, 0)
        self.assertEqual(self.route.duration, 0)
        self.assertEqual(self.route.geodesic_distance_meters, 0)
        self.assertIsNone(self.route.geojson)

    def test_same_location_initialization(self):
        # Test that a ValueError is raised if the two locations are the same
        with self.assertRaises(ValueError):
            Route(self.location1, self.location1, self.api_key)

    @patch("requests.get")
    def test_calculate_route(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "features": [
                {
                    "properties": {
                        "summary": {
                            "distance": 1000,
                            "duration": 600,
                        }
                    }
                }
            ]
        }
        mock_get.return_value = mock_response

        self.route.calculate_route()
        print(self.route.distance)

        # Verify the API call was made correctly
        mock_get.assert_called_with(
            f"https://api.openrouteservice.org/v2/directions/driving-hgv?api_key={self.api_key}&start={self.location1.longitude},{self.location1.latitude}&end={self.location2.longitude},{self.location2.latitude}",
            headers={
                "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
            },
            timeout=600,
        )

        # Check if the distance and duration were updated correctly
        self.assertEqual(self.route.distance, 1000)
        self.assertEqual(self.route.duration, 600)

    def test_geodesic_distance(self):
        # Test the geodesic distance calculation
        distance = self.route.geodesic_distance()
        # Check if the geodesic distance is calculated and returned correctly
        self.assertGreater(distance, 0)
        self.assertEqual(self.route.geodesic_distance_meters, distance)

    # Additional tests can be added to cover other methods and edge cases.


if __name__ == "__main__":
    unittest.main()

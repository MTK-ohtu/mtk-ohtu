import pytest
from unittest.mock import patch
from mtk_ohtu.logic.location import Location

# Test data
ADDRESS = "Exactum, Helsinki"
COORDINATES = (24.961504, 60.204462)  # (longitude, latitude)
INVALID_ADDRESS = "Invalid Address, Nowhere"


@pytest.fixture
def mock_geocode_success():
    with patch("geopy.geocoders.Nominatim.geocode") as mock:
        mock.return_value = type(
            "Loc", (object,), {"latitude": COORDINATES[1], "longitude": COORDINATES[0]}
        )
        yield mock


@pytest.fixture
def mock_geocode_failure():
    with patch("geopy.geocoders.Nominatim.geocode") as mock:
        mock.return_value = None
        yield mock


def test_location_initialization_with_address(mock_geocode_success):
    location = Location(ADDRESS)
    assert location.latitude == COORDINATES[1]
    assert location.longitude == COORDINATES[0]
    assert location.location is not None


def test_location_initialization_with_coordinates():
    location = Location(COORDINATES)
    assert location.latitude == COORDINATES[1]
    assert location.longitude == COORDINATES[0]
    assert location.location is None


def test_location_initialization_with_invalid_input():
    with pytest.raises(ValueError):
        Location(12345)  # Passing an integer to trigger the exception


def test_location_initialization_with_invalid_address(mock_geocode_failure):
    with pytest.raises(ValueError):
        Location(INVALID_ADDRESS)


def test_location_initialization_no_result_found(mock_geocode_failure):
    with pytest.raises(ValueError):
        Location(INVALID_ADDRESS)

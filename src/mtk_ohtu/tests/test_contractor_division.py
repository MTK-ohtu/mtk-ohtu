import pytest
from ..logic.contractor_division import ContractorDivision
from ..logic.location import Location
from ..database.db_datastructs import LogisticsNode, Listing
from ..database.db_enums import CategoryType
import geopy.distance
import random as R
from geojson import FeatureCollection, Feature


product_location = None
delivery_location = None
max_radius = None
distance_mapping = None
mock_listing = None

def random_location():
        random_lat = float(59 + R.random()*11)
        random_lon = float(20 + R.random()*11)
        return Location([random_lon, random_lat])

# Mock method for database access
def db_get_locations_by_cargo_type(cargo_type, db_connection):
    mockList = []
    for i in range(100):
        # Random location for contractor
        location = random_location()
        # Random delivery radius
        random_delivery_radius = R.random() * 800 + 200
        mockList.append(LogisticsNode(
            10, 10, 'address', 'name', location, random_delivery_radius
            ))
    return mockList


# Distance calculator
def distanceBetween(a: Location, b: Location):
    distance = geopy.distance.geodesic(
                (a.latitude, a.longitude),
                (b.latitude, b.longitude)
                ).m / 1000
    return distance

def print_out(l: Location, c: LogisticsNode):
    dist = distanceBetween(l, c.location)
    if (c.delivery_radius >= dist):
        print(f"=== OPTIMAL: delivery radius: {c.delivery_radius}, distance: {dist}")
    else:
        print(f"SUBOPTIMAL: delivery radius: {c.delivery_radius}, distance: {dist}")


@pytest.fixture(scope="function")
def setUp():
    global product_location, delivery_location, mock_listing, division
    # Random locations for product and delivery destination
    product_location = random_location()
    delivery_location = random_location()
    mock_listing = Listing(
        111, 'stuff', float(1000), 'address', 'description', 'seller', product_location
        )
    division = ContractorDivision(mock_listing, 
                                  CategoryType.DIGESTION, 
                                  db_get_locations_by_cargo_type,
                                  delivery_location)
    

def test_lists_contain_viable_logistics_nodes(setUp):
    assert all(type(node) == LogisticsNode for node in division.optimal)
    assert all(type(node) == LogisticsNode for node in division.suboptimal)


def test_optimal_list_contains_only_contractors_within_two_given_range(setUp):
    for c in division.optimal:
        assert(c.delivery_radius >= distanceBetween(product_location, c.location)
            and c.delivery_radius >= distanceBetween(delivery_location, c.location))


def test_suboptimal_list_contains_only_contractors_outside_two_given_range(setUp):
    for c in division.suboptimal:
        assert(c.delivery_radius < distanceBetween(product_location, c.location)
            or c.delivery_radius < distanceBetween(delivery_location, c.location))
    
    
def test_feature_collection_contains_viable_features(setUp):
    optimal_feature_collection = division.get_optimal()
    suboptimal_feature_collection = division.get_suboptimal()
    assert all(type(feature) == Feature for feature in optimal_feature_collection.features)
    assert all(type(feature) == Feature for feature in suboptimal_feature_collection.features)

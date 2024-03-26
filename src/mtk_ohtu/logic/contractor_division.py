import math
import time
from geojson import Point, Feature, FeatureCollection
from ..database.db_contractors import db_get_location_services_by_cargo_type
from .logistics_info import get_logistics_providers_by_range
from ..database.db_enums import CategoryType
from ..config import DATABASE_POOL
from .location import Location
from ..database.db_datastructs import Listing
from dataclasses import asdict
from .route_calculator import Route
from .route_stats import Emissions

class ContractorDivision:

    """
    Given a listing, queries all logistic contractors from DB with correct coargo capability. Finds optimal contractors by range.
    If fiven a delivery location, filters out of range contractors based on both the listing and the delivery location.
    Divides contractors into two lists: suiteable/ rest.
    Creates leaflet compatible featurecollections from these.
    Args:
        listing: Listing
        cargo_type: CargoType
        database_access: ref. to database.db_contractors.db_get_locations_by_cargo_type
        delivery_location: Location
        cargo_capacity: int
    """

    def __init__(
        self,
        listing: Listing,
        cargo_type: CategoryType,
        database_access,
        delivery_location: Location = None,
        cargo_capacity: int = 1e10,
    ):
        self.database_access = database_access
        self.listing = listing
        self.delivery_location = delivery_location
        self.cargo_capacity = cargo_capacity
        self.contractors = database_access(cargo_type, DATABASE_POOL)
        self.optimal = None
        self.suboptimal = None
        self.split_by_range()

    def split_by_range(self):
        """
        Splits all contractors into 'optimal'/'suboptimal' lists by r between customer/contractor
        """
        nodes = self.contractors
        if self.delivery_location is not None:
            self.optimal = get_logistics_providers_by_range(
                self.listing, self.delivery_location, nodes
            )
            self.suboptimal = list(
                filter(lambda x: (x not in self.optimal), self.contractors)
            )
        else:
            self.optimal = nodes
            self.suboptimal = None

    def get_optimal(self):
        """
        Creates featurecollection of contractors listed as 'in range'.
        Returns all if not splitted.
        """
        if self.optimal is None:
            return self.to_featurecollection(self.contractors)
        return self.to_featurecollection(self.optimal)

    def get_suboptimal(self):
        """
        Creates featurecollection of contractors listed as 'out of range'
        Returns all if not splitted.
        """
        if self.suboptimal is None:
            return []
        return self.to_featurecollection(self.suboptimal)

    def filter_by_cargo_capacity(self, cargo_capacity: int):
        """
        Filters contractors by given cargo capacity.
        Args:
            cargo_capacity: int
        """
        self.cargo_capacity = cargo_capacity
        self.optimal = list(
            filter(lambda x: x.cargo_capacity >= cargo_capacity, self.optimal)
        )
        self.suboptimal = list(
            filter(lambda x: x.cargo_capacity >= cargo_capacity, self.suboptimal)
        )

    def filter_by_cargo_type(self, type: CategoryType):
        """
        Filters contractors by given cargo type
        Ars:
            type: CategoryType
        """
        self.contractors = self.database_access(type, DATABASE_POOL)

        # for c in self.contractors:
        #     print(c)
        self.split_by_range()

    def to_featurecollection(self, contractor_list: list):
        """
        Create a feature collection from a list of LogisticsNodes
        Args:
            contractor_list: list(LogisticsNode)
        """
        features = []
        for contractor in contractor_list:
            properties = asdict(contractor)
            del properties['location']
            feature = Feature(
                geometry=Point(
                    (contractor.location.longitude, contractor.location.latitude)
                ),
                properties=properties,
            )
            features.append(feature)
        collection = FeatureCollection(features)

        return collection
    
    def calc_contactor_distance_from_product(self,precise=False):
        """
        Calculates the distance between the contractor's and the product's locations. Precise uses the route API, otherwise geodesic distance.
        Saves the distance (in meters) in the contractor object as dist_to_product and returns it.

        Args:
            presice: bool

        Returns:
            float: distance in meters
        """
        for contractor in self.contractors:
            route = Route(self.listing.location, contractor.location)
            distance = 0
            if precise:
                route.calculate_route()
                distance = route.distance / 1000
            else:
                # use geodesic distance with factor 1.3
                distance = route.geodesic_distance() / 1000 * 1.3
            contractor.dist_to_product = distance
            #print("listing.location:",self.listing.location,"\ncontractor.location:",contractor.location,"\nroute.distance;",route.distance/1000)
        return distance
    
    def calc_contactor_distance_from_delivery(self,precise=False):
        """
        Calculates the distance between the contractor's location and the delivery location. Precise uses the route API, otherwise geodesic distance.
        Saves the distance (in meters) in the contractor object as dist_to_delivery and returns it.

        Args:
            presice: bool

        Returns:
            float: distance in meters
        """
        for contractor in self.contractors:
            route = Route(self.delivery_location, contractor.location)
            distance = 0
            if precise:
                route.calculate_route()
                distance = route.distance / 1000
            else:
                # use geodesic distance with factor 1.3
                distance = route.geodesic_distance() / 1000 * 1.3
            contractor.dist_to_delivery = distance
        return distance

    def calc_emissions_on_route(self, route: Route):
        """
        Calculates the contractors emissions on a route.

        Args:
            route: Route
        
        Returns:
            float: emissions in kg
        """
        for contractor in self.contractors:
            e = Emissions(contractor.fuel, route.distance, contractor.fuel_efficiency)
            emissions = e.calculate_emissions()
            contractor.emissions_on_route = emissions
        return emissions

    def calc_emissions_outside_route(self):
        """
        Calculates the contractors emissions outside the route.

        Returns:
            float: emissions in kg
        """
        for contractor in self.contractors:
            if contractor.dist_to_product is None:
                self.calc_contactor_distance_from_product()
            if contractor.dist_to_delivery is None:
                self.calc_contactor_distance_from_delivery()
            e1 = Emissions(contractor.fuel, contractor.dist_to_product*1000, contractor.fuel_efficiency)
            e2 = Emissions(contractor.fuel, contractor.dist_to_delivery*1000, contractor.fuel_efficiency)
            emissions = e1.calculate_emissions() + e2.calculate_emissions()
            print(f'e1 emission: {e1.calculate_emissions()}, e2 emission: {e2.calculate_emissions()}')
            contractor.emissions_outside_route = emissions
        return emissions
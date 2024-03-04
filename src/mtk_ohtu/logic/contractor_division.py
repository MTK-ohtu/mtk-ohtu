import math
from geojson import Point, Feature, FeatureCollection
from ..database.db_contractors import db_get_logistics
from ..database.db_cargo import db_get_locations_by_cargo_type
from ..database.db_enums import CategoryType
from ..config import DATABASE_POOL


class ContractorDivision:

    """
    Given a coordinate, queries all logistic contractors from DB by given fields.
    Divides contractors into two lists: suiteable/ rest.
    Creates leaflet compatible featurecollections from these
    Args:
        source_lat, source_lon:
    """

    def __init__(self, lat:float, lon:float, cargo_capasity:int = 1e10):
        self.lat = lat
        self.lon = lon
        self.cargo_capasity = cargo_capasity
        self.contractors = db_get_logistics(DATABASE_POOL)
        self.optimal = None
        self.suboptimal = None

    def split_by_range(self):
        """
        Splits all contractors into 'optimal'/'suboptimal' lists by r between customer/contractor
        Args:
            latitude: float
            longitude: float
        """
        self.optimal = list(
            filter(
                lambda x: (
                    self.haversine(
                        self.lat,
                        self.lon,
                        x.location.latitude,
                        x.location.longitude,
                    )
                )
                < x.delivery_radius,
                self.contractors,
            )
        )
        self.suboptimal = list(
            filter(
                lambda x: (
                    self.haversine(
                        self.lat,
                        self.lon,
                        x.location.latitude,
                        x.location.longitude,
                    )
                )
                > x.delivery_radius,
                self.contractors,
            )
        )

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
            return self.to_featurecollection(self.contractors)
        return self.to_featurecollection(self.suboptimal)
        
    

    def filter_by_cargo_capasity(self, cargo_capacity: int):
        """
        Filters contractors by given cargo capacity.
        Args:
            cargo_capacity: int
        """
        self.cargo_capasity = cargo_capacity
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
        self.contractors = db_get_locations_by_cargo_type(type, DATABASE_POOL)
        self.split_by_range



    def to_featurecollection(self, contractor_list: list):
        """
        Create a feature collection from a list of LogisticsNodes
        Args:
            contractor_list: list(LogisticsNode)
        """
        features = []
        for contractor in contractor_list:
            properties = {"name": contractor.name, "address": contractor.address}
            feature = Feature(
                geometry=Point(
                    (contractor.location.longitude, contractor.location.latitude)
                ),
                properties=properties,
            )
            features.append(feature)
        collection = FeatureCollection(features)

        return collection


    def haversine(self, lat1, lon1, lat2, lon2):
        """
        Calculate great-circle distances
        """
        dLat = (lat2 - lat1) * math.pi / 180.0
        dLon = (lon2 - lon1) * math.pi / 180.0
        lat1 = (lat1) * math.pi / 180.0
        lat2 = (lat2) * math.pi / 180.0
        a = pow(math.sin(dLat / 2), 2) + pow(math.sin(dLon / 2), 2) * math.cos(
            lat1
        ) * math.cos(lat2)
        rad = 6371
        c = 2 * math.asin(math.sqrt(a))
        return float(rad * c)
    

    


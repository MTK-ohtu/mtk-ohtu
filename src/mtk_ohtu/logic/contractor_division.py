import math
from geojson import Point, Feature, FeatureCollection
from ..database.database import db_get_logistics
from ..config import DATABASE_POOL

class ContractorDivision:

    """
    Given a coordinate, queries all logistic contractors from DB by given fields.
    Divides contractors into two lists: suiteable/ rest.
    Creates leaflet compatible featurecollections from these
    Args:
        source_lat, source_lon:
    """

    def __init__(self, fields: list):
        self.contractors = db_get_logistics(DATABASE_POOL)
        self.optimal = None
        self.suboptimal = None
        self.fields = fields

    def split_by_range(self, source_lat: float, source_lon: float, driver_range: float):
        """
        Splits all contractors into 'optimal'/'suboptimal' lists by given
        Args:
            latitude: float
            longitude: float
            limit: float, straight line distance in kilometers
        Return: tuple (list1, list2), first containing contractors inside range, second contains the rest 
        """
        self.optimal = list(
            filter(
                lambda x: (
                    self.haversine(
                        source_lat,
                        source_lon,
                        x.location.latitude,
                        x.location.longitude,
                    )
                )
                < driver_range,
                self.contractors,
            )
        )
        self.suboptimal = list(
            filter(
                lambda x: (
                    self.haversine(
                        source_lat,
                        source_lon,
                        x.location.latitude,
                        x.location.longitude,
                    )
                )
                > driver_range,
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
        collection = self.to_featurecollection(self.optimal)
        return collection

    def get_suboptimal(self):
        """
        Creates featurecollection of contractors listed as 'out of range'
        Returns all if not splitted.
        """
        if self.suboptimal is None:
            return self.to_featurecollection(self.contractors)
        collection = self.to_featurecollection(self.suboptimal)
        return collection

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

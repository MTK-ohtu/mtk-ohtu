from ..database.database import db_get_logistics, db_get_contractors_by_fields
from geojson import Point, Feature, FeatureCollection
from flask import jsonify
import math
from ..config import DATABASE_POOL
from geopy.distance import geodesic

class ContractorList:

    def __init__(self, source_lat, source_lon, fields: list):
        self.lat = source_lat
        self.lon = source_lon
        self.contractors = db_get_contractors_by_fields(fields, DATABASE_POOL)
        self.in_range = None
        self.out_range = None    
    '''
    Splits all contractors for out range and in range lists
    Args:
        latitude: float
        longitude: float
        limit: float, straight line distance in kilometers
    Return: tuple (pair) of lists, first containing contractors inside range, second contains the rest 
    '''
    
    def split_by_range(self, range: float):
        self.in_range = list(filter(lambda x: (self.haversine(self.lat, self.lon, x[2], x[3])) < range, self.contractors))
        self.out_range = list(filter(lambda x: (self.haversine(self.lat, self.lon, x[2], x[3])) > range, self.contractors))

    def get_all(self):
        return self.to_featurecollection(self.contractors)

    def get_in_range(self):
        if self.in_range is None:
            return self.to_featurecollection(self.contractors)
        collection = self.to_featurecollection(self.in_range)
        return collection
    
    def get_out_range(self):
        if self.in_range is None:
            return self.to_featurecollection(self.contractors)
        collection = self.to_featurecollection(self.out_range)
        return collection

    def to_featurecollection(self, div: list):
        features = []
        for contractor in div:
            properties = {'name':contractor[0], 'address': contractor[1]}
            feature = Feature(
                geometry=Point((contractor[3], contractor[2])),
                properties=properties
            )
            features.append(feature)
        collection = FeatureCollection(features)
        print(collection)
        return collection

    def haversine(self, lat1, lon1, lat2, lon2):
        dLat = (lat2 - lat1) * math.pi / 180.0
        dLon = (lon2 - lon1) * math.pi / 180.0
        lat1 = (lat1) * math.pi / 180.0
        lat2 = (lat2) * math.pi / 180.0
        a = (pow(math.sin(dLat / 2), 2) +
            pow(math.sin(dLon / 2), 2) *
                math.cos(lat1) * math.cos(lat2))
        rad = 6371
        c = 2 * math.asin(math.sqrt(a))
        return float(rad * c)       
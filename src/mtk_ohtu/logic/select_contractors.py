from ..database.database import db_get_contractors_by_fields
from geojson import Point, Feature, FeatureCollection
import math



def __init__(self):
    self.in_range = []
    self.out_range =[]    
    
'''
Splits all contractors for out range and in range lists
Args:
    latitude: float
    longitude: float
    limit: float, straight line distance in kilometers
Return: tuple (pair) of lists, first containing contractors inside range, second contains the rest 
'''
def split_contractors_by_range(self, lat: float, lon: float, range: float):
    results = db_get_contractors_by_fields(['name', 'address', 'longitude', 'latitude'])
    self.in_range = list(filter(lambda x: haversine(x[2],x[3]) <= range, results))
    self.out_range = list(filter(lambda x: haversine(x[2],x[3]) > range, results))
    
    

def haversine(lat1, lon1, lat2, lon2):
     
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2));
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c
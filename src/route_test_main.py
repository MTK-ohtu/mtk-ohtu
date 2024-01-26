from route_calculator import Route

from location import Location
from geopy.geocoders import Nominatim

# Uses the Route class from route.py. Can be used for testing and should be deleted when the Route class is implemented in the main program.

loc1 = "Gustaf Hällströmin katu 2, 00560 Helsinki"
loc2 = "Leppäsuonkatu 11"
email = "miko.paajanen@helsinki.fi"

geolocator = Nominatim(user_agent=email)


start = Location(loc1, geolocator)
end = Location(loc2, geolocator)

demo_route = Route(loc1,loc2,email)

print(demo_route.distance)
print(demo_route.duration)
print(demo_route.geodesic_distance())


print(f'start: {start.longitude}, {start.latitude}')
print(f'end: {end.longitude}, {end.latitude}')

print(demo_route.geojson)
print(type(demo_route.geojson))

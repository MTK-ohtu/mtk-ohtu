from logic.route_calculator import Route
from logic.location import Location
from geopy.geocoders import Nominatim
import database.database as db
from config import DATABASE_CONFIG


# Uses the Route class from route.py. Can be used for testing and should be deleted when the Route class is implemented in the main program.

loc1 = "Gustaf Hällströmin katu 2, 00560 Helsinki"
loc2 = "Leppäsuonkatu 11"
email = "miko.paajanen@helsinki.fi"

geolocator = Nominatim(user_agent=email)


start = Location(loc1, email)
end = Location(loc2, email)

demo_route = Route(loc1,loc2,email)

print(demo_route.distance)
print(demo_route.duration)
print(demo_route.geodesic_distance())


print(f'start: {start.longitude}, {start.latitude}')
print(f'end: {end.longitude}, {end.latitude}')

#print(demo_route.geojson))

print(db.db_get_product_list(DATABASE_CONFIG))
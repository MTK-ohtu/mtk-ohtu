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

print(start.location.raw)

# demo_route = Route(loc1,loc2,email)


# print(demo_route.distance)
# print(demo_route.duration)
# print(demo_route.geodesic_distance())


# print(f'start: {start.longitude}, {start.latitude}')
# print(f'end: {end.longitude}, {end.latitude}')

#print(demo_route.geojson))


# listings = db.db_get_product_list(DATABASE_CONFIG)
# for i in range(12):
#     print(listings[i])


# counting_set = set(listings)
# unique_listings = len(counting_set)
# print(counting_set)


# print()
# print("sql")
# print()
# for listing in counting_set:
#     loc = Location(listing[2], email)
#     print(f"INSERT INTO products (seller_id, name, price, description, image, created_at, location, coordinates) VALUES ({listing[4][-1]}, '{listing[0]}', {listing[1]}, '{listing[3]}', NULL, NOW(), '{listing[2]}', [{loc.longitude}, {loc.latitude}]) ON CONFLICT DO NOTHING;")



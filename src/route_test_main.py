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


listings = db.db_get_product_list(DATABASE_CONFIG)
unique_listings = []

for listing in listings:
    if listing not in unique_listings:
        unique_listings.append(listing)

# counting_set = set(listings)
# unique_listings = len(counting_set)
# print(counting_set)


# print()
# print("sql")
# print()
# for listing in counting_set:
#     loc = Location(listing[2], email)
#     print(f"INSERT INTO products (seller_id, name, price, description, image, created_at, location, coordinates) VALUES ({listing[4][-1]}, '{listing[0]}', {listing[1]}, '{listing[3]}', NULL, NOW(), '{listing[2]}', ST_GeomFromText('POINT({loc.longitude} {loc.latitude})', 4326)) ON CONFLICT DO NOTHING;")


A = unique_listings[0]
B = unique_listings[2]
for i in range(7):
    print(f'{i}: {A[i]}')

loc_A = Location((A[5], A[6]))
loc_B = Location((B[5], B[6]))



test_route = Route(loc_A,loc_B)
print("test_route")
print(test_route.distance)
print(test_route.duration)
print(test_route.geodesic_distance())
from logic.route_calculator import Route, FuelType
from logic.location import Location
from geopy.geocoders import Nominatim
import database.database as db
from config import DATABASE_CONFIG
import time


# Uses the Route class from route.py. Can be used for testing and should be deleted when the Route class is implemented in the main program.

loc1 = "Gustaf Hällströmin katu 2, 00560 Helsinki"
loc2 = "Leppäsuonkatu 11"
email = "miko.paajanen@helsinki.fi"

geolocator = Nominatim(user_agent=email)


# start = Location(loc1, email)
# end = Location(loc2, email)

# print(start.location.raw)

# demo_route = Route(loc1,loc2,email)


# print(demo_route.distance)
# print(demo_route.duration)
# print(demo_route.geodesic_distance())


# print(f'start: {start.longitude}, {start.latitude}')
# print(f'end: {end.longitude}, {end.latitude}')

# print(demo_route.geojson))


# listings = db.db_get_product_list(DATABASE_CONFIG)
# unique_listings = []

# for listing in listings:
#     if listing not in unique_listings:
#         unique_listings.append(listing)


# print(len(unique_listings))
# for listing in unique_listings:
#     if listing[5] is not None and listing[6] is not None:
#         print(listing[2],":",listing[5],listing[6])
#         print(type(listing[5]))
#         loc = Location((listing[5],listing[6]))
#         print("coords (lon, lat):",loc.longitude, loc.latitude)


# print()
# print("sql")
# print()
# for listing in counting_set:
#     loc = Location(listing[2], email)
#     print(f"INSERT INTO products (seller_id, name, price, description, image, created_at, location, coordinates) VALUES ({listing[4][-1]}, '{listing[0]}', {listing[1]}, '{listing[3]}', NULL, NOW(), '{listing[2]}', ST_GeomFromText('POINT({loc.longitude} {loc.latitude})', 4326)) ON CONFLICT DO NOTHING;")


# A = unique_listings[0]
# B = unique_listings[2]
# for i in range(7):
#     print(f"{i}: {A[i]}")

# loc_A = Location((A[5], A[6]))
# loc_B = Location((B[5], B[6]))


# test_route = Route(loc_A, loc_B)
# print("test_route")
# print(test_route.distance)
# print(test_route.duration)

# start_time = time.time()
# print(test_route.geodesic_distance())
# print(test_route.geodesic_distance())
# print("geodesic distance calculation", time.time() - start_time)

# start_time = time.time()
# test_route.calculate_route()
# print(test_route.distance)
# print(test_route.duration)
# print("route calculation", time.time() - start_time)

loc1 = Location((24.962548,60.205298))
loc2 = Location((25.571514,64.977991))
print(loc1.latitude)
route = Route(loc1, loc2)
route.calculate_route()
print(route.distance)
print(route.duration)
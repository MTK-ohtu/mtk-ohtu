from route import Route
# Uses the Route class from route.py. Can be used for testing and should be deleted when the Route class is implemented in the main program.

loc1 = "Gustaf Hällströmin katu 2, 00560 Helsinki"
loc2 = "Leppäsuonkatu 11"
email = "miko.paajanen@helsinki.fi"

demo_route = Route(loc1,loc2,email)

print(demo_route.distace)
print(demo_route.duration)
print(demo_route.geodesic_distance())
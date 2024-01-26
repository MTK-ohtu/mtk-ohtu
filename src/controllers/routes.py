from flask import Blueprint, render_template, request, redirect
import route_calculator
import datetime

controller = Blueprint("example", __name__)

@controller.route("/")
def index():
    return render_template("index.html")

@controller.route("/listings")
def listings():
    user_location = "Helsinki"
    listing1_location = "Turku"
    listing2_location = "Kemi"
    route1 = route_calculator.Route(user_location, listing1_location, "miko.paajanen@helsinki.fi")
    route2 = route_calculator.Route(user_location, listing2_location, "miko.paajanen@helsinki.fi")
    return render_template(
        "listings.html",
        distance1=round(route1.distance/1000,1),
        distance2=round(route2.distance/1000,1),
    )

@controller.route("/createpost")
def create_listing():
    return render_template("createpost.html")

@controller.route("/login")
def login():
    return render_template("login.html")


@controller.route("/distance", methods=["get", "post"])
def distance():
    if request.method == "GET":
        return render_template("distance.html", start_location = (0,0), end_location=(0,0))
    if request.method == "POST":
        address1 = request.form["address1"]
        address2 = request.form["address2"]
        qt = int(request.form["quantity"])
        route = route_calculator.Route(address1, address2, "miko.paajanen@helsinki.fi")
        start_location = (route.location1.latitude, route.location1.longitude)
        end_location = (route.location2.latitude, route.location2.longitude)

        return render_template(
            "distance.html",
            distance=round(route.distance/1000,1), 
            #"duration=str(datetime.timedelta(seconds=(route.duration))).split(".")[0],
            duration=str(datetime.timedelta(seconds=(round(route.duration)))),
            geodesic_distance=round(route.geodesic_distance()/1000,1),
            price = round(route.distance/1000,1)*qt*0.5,
            start_location = start_location,
            end_location = end_location,
            route_geojson = route.geojson
        )
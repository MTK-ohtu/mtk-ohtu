from flask import Blueprint, render_template, request, redirect
from config import DATABASE_CONFIG
import database.database as db
import logic.route_calculator as route_calculator
import datetime
import logic.user as users

controller = Blueprint("example", __name__)


@controller.route("/")
def index():
    return render_template("index.html")


@controller.route("/listings")
def listings():
    user_location = "Simonkatu 6"
    db_listings = db.db_get_product_list(DATABASE_CONFIG)
    print(len(db_listings))
    listings = []
    i = 0
    for listing in db_listings:
        print(f'{listing[0]}: {listing[2]}')
        listings.append(
            {
                "name": listing[0],
                "price": listing[1],
                "location": listing[2],
                "seller": listing[3],
                "distance": round(route_calculator.Route(
                    user_location, listing[2]
                ).distance / 1000, 1),
            }
        )
        i += 1
        if i > 10:
            break

    return render_template(
        "listings.html",
        listings=listings,
    )


@controller.route("/createpost")
def create_listing():
    return render_template("createpost.html")


@controller.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", message="Salasana tai käyttäjätunnus väärin")

@controller.route("/distance", methods=["get", "post"])
def distance():
    if request.method == "GET":
        return render_template(
            "distance.html", start_location=(0, 0), end_location=(0, 0)
        )
    if request.method == "POST":
        address1 = request.form["address1"]
        address2 = request.form["address2"]
        qt = int(request.form["quantity"])
        route = route_calculator.Route(address1, address2, "miko.paajanen@helsinki.fi")
        start_location = (route.location1.latitude, route.location1.longitude)
        end_location = (route.location2.latitude, route.location2.longitude)

        return render_template(
            "distance.html",
            distance=round(route.distance / 1000, 1),
            # "duration=str(datetime.timedelta(seconds=(route.duration))).split(".")[0],
            duration=str(datetime.timedelta(seconds=(round(route.duration)))),
            geodesic_distance=round(route.geodesic_distance()/1000,1),
            price = round(route.distance/1000*qt*0.5,2),
            start_location = start_location,
            end_location = end_location,
            route_geojson = route.geojson
        )

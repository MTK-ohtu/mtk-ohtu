from flask import Blueprint, render_template, request, redirect
from config import DATABASE_CONFIG
import database.database as db
import logic.route_calculator as route_calculator
from logic.location import Location
import datetime
import logic.user as users
import logic.logistics as logistics

controller = Blueprint("example", __name__)


@controller.route("/")
def index():
    return render_template("index.html")


@controller.route("/listings", methods=["GET", "POST"])
def listings():
    db_listings = db.db_get_product_list(DATABASE_CONFIG)
    if request.method == "POST":
        user_location = Location(request.form["address"])
    listings = []     
    for listing in db_listings:
        if request.method == "GET": 
            listings.append(
                {
                    "name": listing[0],
                    "price": listing[1],
                    "location": listing[2],
                    "seller": listing[3],
                    "distance": "Submit location to see distance in",
                }
            )
        if request.method == "POST":
            listing_location = Location(listing[2])
            route_to_product = route_calculator.Route(
                user_location, listing_location
            )
            listings.append(
                {
                    "name": listing[0],
                    "price": listing[1],
                    "location": listing[2],
                    "seller": listing[3],
                    "distance": round(route_to_product.geodesic_distance() / 1000, 1),
                }
            )
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
        address1 = Location(request.form["address1"])
        address2 = Location(request.form["address2"])
        qt = int(request.form["quantity"])
        route = route_calculator.Route(address1, address2)
        route.calculate_route()
        start_location = (route.location1.latitude, route.location1.longitude)
        end_location = (route.location2.latitude, route.location2.longitude)

        return render_template(
            "distance.html",
            distance=round(route.distance / 1000, 1),
            duration=str(datetime.timedelta(seconds=(round(route.duration)))),
            geodesic_distance=round(route.geodesic_distance()/1000,1),
            price = round(route.distance/1000*qt*0.5,2),
            start_location = start_location,
            end_location = end_location,
            route_geojson = route.geojson
        )


@controller.route("/addlogistics", methods=["GET", "POST"])
def add_logistics():
    if request.method == "GET":
        return render_template("addlogistics.html")
    
    if request.method == "POST":
        service_type = request.form.get('serviceType')
        name = request.form.get('fullName') if service_type == 'private' else request.form.get('companyName')
        business_id = request.form.get('businessId') if service_type == 'company' else None
        address = request.form.get('address')
        vehicle_categories = request.form.getlist('vehicleCategories[]')

        logistics.addlogistics(service_type, name, business_id, address, vehicle_categories)

        return redirect("/")

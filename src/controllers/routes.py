from flask import Blueprint, render_template, request, redirect, url_for
from config import DATABASE_POOL
import database.database as db
import logic.route_calculator as route_calculator
from logic.location import Location
import datetime
import logic.user as users
import logic.logistics as logistics
from database.db_enums import CategoryType
import controllers.session_handler as session_handler
import logic.route_stats as route_stats

controller = Blueprint("example", __name__)


@controller.route("/")
def index():
    return render_template("index.html")


@controller.route("/listings", methods=["GET", "POST"])
def listings():
    db_listings = db.db_get_product_list(DATABASE_POOL)
    if request.method == "POST":
        user_location = Location(request.form["address"])
    listings = []
    for listing in db_listings:
        if request.method == "GET":
            listings.append(
                {
                    "listing_id": listing[7],
                    "name": listing[0].value,
                    "price": listing[1],
                    "location": listing[2],
                    "seller": listing[3],
                    "distance": "Submit location to see distance in",
                }
            )
        if request.method == "POST":
            start_time = datetime.datetime.now()
            if listing[5] is not None and listing[6] is not None:
                listing_location = Location((listing[5], listing[6]))
                print(
                    "calc with coords: ",
                    (datetime.datetime.now() - start_time).microseconds / 1000,
                    "ms",
                )

            else:
                listing_location = Location(listing[2])
                print(
                    "calc with address:",
                    (datetime.datetime.now() - start_time).microseconds / 1000,
                    "ms",
                )
            route_to_product = route_calculator.Route(user_location, listing_location)
            listings.append(
                {
                    "listing_id": listing[7],
                    "name": listing[0].value,
                    "price": listing[1],
                    "location": listing[2],
                    "seller": listing[3],
                    "distance": round(route_to_product.geodesic_distance() / 1000, 1),
                }
            )
            listings = sorted(listings, key=lambda x: x['distance'])
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
            return render_template(
                "login.html", message="Salasana tai käyttäjätunnus väärin"
            )
        
@controller.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@controller.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        if users.register(username, password, email):
            return redirect("/")
        else:
            return render_template(
                "register.html", message="Käyttäjätunnus on jo käytössä"
            )

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
            geodesic_distance=round(route.geodesic_distance() / 1000, 1),
            price=round(route.distance / 1000 * qt * 0.5, 2),
            start_location=start_location,
            end_location=end_location,
            route_geojson=route.geojson,
        )


@controller.route("/addlogistics", methods=["GET", "POST"])
def add_logistics():
    if request.method == "GET":

        material_categories = [e.value for e in CategoryType]
        return render_template(
            "addlogistics.html",
            material_categories=material_categories
        )

    if request.method == "POST":
        service_type = request.form.get("serviceType")
        name = (
            request.form.get("fullName")
            if service_type == "private"
            else request.form.get("companyName")
        )
        business_id = (
            request.form.get("businessId") if service_type == "company" else None
        )
        address = request.form.get("address")
        radius = request.form.get("radius")
        categories = request.form.getlist("materials[]")
        base_rates = request.form.getlist("base_rates[]")
        prices_per_hour = request.form.getlist("prices_per_hour[]")

        if logistics.addlogistics(service_type, name, business_id, address, radius, categories, base_rates, prices_per_hour):
            return redirect(url_for('example.confirmation', message='Logistics submitted successfully'))
        else:
            return redirect(url_for('example.confirmation', message='An error occurred while submitting logistics'))

@controller.route("/confirmation")
def confirmation():
    message = request.args.get('message', 'Confirmation message not provided')
    return render_template("confirmation.html", message=message)


@controller.route("/listing/<int:listing_id>", methods=["GET", "POST"])
def listing(listing_id):
    if request.method == "GET":
        db_listing = db.db_get_product_by_id(listing_id, DATABASE_POOL)
        print(db_listing)
        listing = {
            "name": db_listing[0].value,
            "price": db_listing[1],
            "address": db_listing[2],
            "description": db_listing[3],
            "seller": db_listing[4],
            "longitude": db_listing[5],
            "latitude": db_listing[6],
        }
        return render_template(
            "product.html", listing=listing, listing_id=listing_id, show_route=False
        )
    if request.method == "POST":
        db_listing = db.db_get_product_by_id(listing_id, DATABASE_POOL)
        listing = {
            "name": db_listing[0].value,
            "price": db_listing[1],
            "address": db_listing[2],
            "description": db_listing[3],
            "seller": db_listing[4],
            "longitude": db_listing[5],
            "latitude": db_listing[6],
        }
        user_location = Location(request.form["address"])
        if listing["longitude"] is not None and listing["latitude"] is not None:
            listing_location = Location((listing["longitude"], listing["latitude"]))
        else:
            listing_location = Location(listing["address"])
        route_to_product = route_calculator.Route(listing_location, user_location)
        route_to_product.calculate_route()
        session_handler.save_route_to_session(route_to_product)
        print(session_handler.get_route_from_session()["distance"])
        logistics_db = db.db_get_logistics(DATABASE_POOL)
        companies = []
        for company in logistics_db:
            companies.append(
                {
                    "name": company[2],
                    "address": company[5],
                    "radius": company[-1],
                    "id": company[0],
                }
            )

        return render_template(
            "product.html",
            listing_id=listing_id,
            listing=listing,
            distance=round(route_to_product.distance / 1000, 1),
            duration=str(
                datetime.timedelta(seconds=(round(route_to_product.duration)))
            ),
            route_geojson=route_to_product.geojson,
            user_location=user_location.location,
            companies=companies,
            show_route=True,
        )

@controller.route("/contractors", methods=["GET"])
def get_contractors(x,y,r):
    contractors = db.get_contractors_by_euclidean(x, y, r, DATABASE_POOL)
    return render_template("contractor_list.html", x, y, contractors)


@controller.route("/submit_emission_info", methods=["POST"])
def submit_emission_info():
    if request.method == "POST":
        fuel = request.form["fuelType"]
        fuel_consumption = request.form["fuel_efficiency"]
        listing_id = request.form["listing_id"]
        distance = session_handler.get_route_from_session()["distance"]
        emissions = route_stats.calculate_emissions(fuel, fuel_consumption, distance)
        return render_template("product.html", emissions=emissions)
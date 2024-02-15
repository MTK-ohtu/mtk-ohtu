import datetime
import database.database as db
import logic.route_calculator as route_calculator
import logic.session_handler as session_handler
import logic.route_stats as route_stats
from flask import Blueprint, render_template, request, redirect
from config import DATABASE_POOL
from logic.location import Location


listing_bp = Blueprint("listing_bp", __name__)


@listing_bp.route("/")
def index():
    return render_template("index.html")


@listing_bp.route("/listings", methods=["GET", "POST"])
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


@listing_bp.route("/createpost")
def create_listing():
    return render_template("createpost.html")


@listing_bp.route("/listing/<int:listing_id>", methods=["GET", "POST"])
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
            "product.html", listing=listing, listing_id=listing_id, show_route=False, consumption=55
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
        #print(session_handler.get_route_from_session()["location2"]["location"])
        fuel = request.form["fuelType"]
        fuel_consumption = request.form["fuel_efficiency"]
        emissions = route_stats.calculate_emissions(fuel, route_to_product.distance,fuel_consumption)
        logistics_db = db.db_get_logistics(DATABASE_POOL)
        companies = []
        for company in logistics_db:
            companies.append(
                {
                    "name": company[2],
                    "address": company[5],
                    "radius": company[-1],
                    "id": company[0],
                    "longitude": company[6],
                    "latitude": company[7],
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
            emissions=round(emissions),
            companies=companies,
            consumption=fuel_consumption,
            show_route=True,
        )
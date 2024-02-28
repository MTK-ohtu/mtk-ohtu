import datetime

import mtk_ohtu.database.db_listings
from ..database import db_contractors as db
from ..database import db_cargo as cargo_db
from ..logic import route_calculator
from ..logic import session_handler
from ..logic import route_stats
from flask import Blueprint, render_template, request, redirect
from ..config import DATABASE_POOL
from ..logic.location import Location
from ..database.db_datastructs import Listing
from ..logic.contractor_division import ContractorDivision
from ..logic.logistics_info import get_logistics_providers, get_logistics_info

listing_bp = Blueprint("listing_bp", __name__)


@listing_bp.route("/")
def index():
    return render_template("index.html")


@listing_bp.route("/listings", methods=["GET", "POST"])
def listings():
    listings = mtk_ohtu.database.db_listings.db_get_product_list(DATABASE_POOL)
    distances = {}

    if request.method == "GET":
        for listing in listings:
            distances[listing.id] = "Submit address to get a distance estimate"

    if request.method == "POST":
        user_location = Location(request.form["address"])
        for listing in listings:
            route_to_product = route_calculator.Route(user_location, listing.location)
            distances[listing.id] = round(
                route_to_product.geodesic_distance() / 1000, 1
            )

        listings = sorted(listings, key=lambda x: distances[x.id])

    return render_template("listings.html", listings=listings, distances=distances)


@listing_bp.route("/createpost")
def create_listing():
    return render_template("createpost.html")


def get_url_for_listing(listing: Listing) -> str:
    return request.url_root + "listing/" + str(listing.id)


@listing_bp.route("/listing/<int:listing_id>", methods=["GET", "POST"])
def listing(listing_id):
    if request.method == "GET":
        
        db_listing = mtk_ohtu.database.db_listings.db_get_product_by_id(listing_id, DATABASE_POOL)
        contractors = ContractorDivision()
        contractors.split_by_range(float(db_listing.location.latitude), float(db_listing.location.longitude))
        return render_template(
            "product.html",
            listing=db_listing,
            listing_id=listing_id,
            show_route=False,
            consumption=55,
            in_range=contractors.get_optimal(),
            out_range=contractors.get_suboptimal(),
            lat=db_listing.location.latitude,
            lon=db_listing.location.longitude,
            logistics_info=(0, 0)
        )

    if request.method == "POST":
        listing = mtk_ohtu.database.db_listings.db_get_product_by_id(listing_id, DATABASE_POOL)
        user_location = Location(request.form["address"])
        route_to_product = route_calculator.Route(listing.location, user_location)
        route_to_product.calculate_route()
        session_handler.save_route_to_session(route_to_product)
        fuel = request.form["fuelType"]
        fuel_consumption = request.form["fuel_efficiency"]
        emissions = route_stats.calculate_emissions(
            fuel, route_to_product.distance, fuel_consumption
        )
        logistics_nodes = db.db_get_logistics(DATABASE_POOL)
        
        logistics_info = get_logistics_info(listing, user_location)
        print("LOGISTICS INFO:",logistics_info)

        contractors = ContractorDivision()
        contractors.split_by_range(float(listing.location.latitude), float(listing.location.longitude))

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
            companies=logistics_nodes,
            consumption=fuel_consumption,
            show_route=True,
            in_range=contractors.get_optimal(),
            out_range=contractors.get_suboptimal(),
            lat=listing.location.latitude,
            lon=listing.location.longitude,
            logistics_info=logistics_info
        )

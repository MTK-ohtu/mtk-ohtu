import datetime
from flask import Blueprint, render_template, request, redirect, abort
from flask_babel import _
import mtk_ohtu.database.db_listings
from ..database import db_contractors as db
from ..database import db_cargo as cargo_db
from ..logic import route_calculator
from ..logic import session_handler
from ..logic.route_stats import Emissions
from ..config import DATABASE_POOL, BUILD_DATE
from ..logic.location import Location
from ..database.db_datastructs import Listing
from ..database.db_contractors import db_get_location_services_by_cargo_type
from ..logic.contractor_division import ContractorDivision
from ..logic.logistics_info import get_logistics_providers, get_logistics_info

listing_bp = Blueprint("listing_bp", __name__)


@listing_bp.route("/listings", methods=["GET", "POST"])
def listings():
    listings = mtk_ohtu.database.db_listings.db_get_product_list(DATABASE_POOL)
    distances = {}

    if request.method == "GET":
        for listing in listings:
            distances[listing.id] = _("submit_address_first")

    if request.method == "POST":
        user_location = Location(request.form["address"])
        for listing in listings:
            route_to_product = route_calculator.Route(user_location, listing.location)
            distances[listing.id] = str(round(
                route_to_product.geodesic_distance() / 1000, 1
            )) + " " + _("km")

        listings = sorted(listings, key=lambda x: distances[x.id])

    return render_template(
        "listings.html", listings=listings, distances=distances
    )


@listing_bp.route("/createpost")
def create_listing():
    return render_template("createpost.html")


def get_url_for_listing(listing: Listing) -> str:
    return request.url_root + "listing/" + str(listing.id)


@listing_bp.route("/listing/<int:listing_id>", methods=["GET", "POST"])
def listing(listing_id):
    listing = mtk_ohtu.database.db_listings.db_get_product_by_id(
        listing_id, DATABASE_POOL
    )
    if not listing:
        abort(404) 

    if request.method == "GET":
        # contractors = ContractorDivision(float(listing.location.latitude), float(listing.location.longitude), listing.category)
        contractors = ContractorDivision(
            listing, listing.category, db_get_location_services_by_cargo_type, listing.location
        )
        # contractors.filter_by_cargo_type(listing.category)
        return render_template(
            "product.html",
            listing=listing,
            show_route=0,
            user_location=None,
            consumption=55,
            in_range=contractors.get_optimal(),
            out_range=contractors.get_suboptimal(),
        )

    if request.method == "POST":
        user_location = Location(request.form["address"])
        print("user_locaton",user_location)
        route_to_product = route_calculator.Route(listing.location, user_location)
        route_to_product.calculate_route()
        session_handler.save_route_to_session(route_to_product)
        fuel = request.form["fuelType"]
        fuel_consumption = request.form["fuel_efficiency"]
        emission_info = Emissions(fuel, route_to_product.distance, fuel_consumption)
        emissions = emission_info.calculate_emissions()
        emission_comparison = emission_info.get_emissions_for_all_fuels()
        # contractors = ContractorDivision(float(listing.location.latitude), float(listing.location.longitude), listing.category)
        contractors = ContractorDivision(
            listing, listing.category, db_get_location_services_by_cargo_type, user_location
        )
        # contractors.filter_by_cargo_type(listing.category)

        return render_template(
            "product.html",
            listing=listing,
            distance=round(route_to_product.distance / 1000, 1),
            duration=str(
                datetime.timedelta(seconds=(round(route_to_product.duration)))
            ),
            route_geojson=route_to_product.geojson,
            user_location=user_location.location,
            emissions=emissions,
            emission_comparison=emission_comparison,
            consumption=fuel_consumption,
            show_route=1,
            in_range=contractors.get_optimal(),
            out_range=contractors.get_suboptimal(),
        )

import math
from flask import Blueprint, render_template, request, redirect, url_for, abort, session
from geojson import Point, Feature, FeatureCollection
from ..database.db_enums import CategoryType
from ..config import DATABASE_POOL
from ..logic import user as users
from ..logic import logistics
from ..database import database as db
from ..logic.contractor_division import ContractorDivision

contractor_bp = Blueprint("contractor_bp", __name__)


@contractor_bp.route("/addlogistics", methods=["GET", "POST"])
def add_logistics():
    if request.method == "GET":
        material_categories = [e.value for e in CategoryType]
        return render_template(
            "addlogistics.html", material_categories=material_categories
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
        user_id = users.user_id()
        address = request.form.get("address")
        radius = request.form.get("radius")
        categories = request.form.getlist("materials[]")
        base_rates = request.form.getlist("base_rates[]")
        prices_per_hour = request.form.getlist("prices_per_hour[]")
        maximum_capacities = request.form.getlist("max_capacities[]")
        maximum_distances = request.form.getlist("max_distances[]")
        telephone = "4039"
        email = "s"

        contractor_id = logistics.add_contractor(user_id, name, business_id)
        contractor_location_id = logistics.add_contractor_location(contractor_id, address, telephone, email, radius)
        logistics.add_cargo_capability(contractor_location_id, categories, base_rates, prices_per_hour, maximum_capacities, maximum_distances)

        session["contractor_id"] = contractor_id
        return redirect(
            url_for(
                "contractor_bp.confirmation",
                message="Logistics submitted successfully",
            )
        )


@contractor_bp.route("/confirmation")
def confirmation():
    message = request.args.get("message", "Confirmation message not provided")
    return render_template("confirmation.html", message=message)


@contractor_bp.route("/contractors", methods=["GET"])
def get_contractors(x, y, r):
    contractors = db.get_contractors_by_euclidean(x, y, r, DATABASE_POOL)
    return render_template("contractor_list.html", x, y, contractors)


@contractor_bp.route("/contractor", methods=["GET"])
def contractor():
    if request.method == "GET":
        user_id = users.user_id()
        contractor_db = db.db_get_contractor(user_id, DATABASE_POOL)
        if not contractor_db:
            return redirect("/addlogistics")

        cargo_prices = db.db_get_cargo_prices(contractor_db.id, DATABASE_POOL)
        return render_template(
            "contractor.html", contractor=contractor_db, cargo_prices=cargo_prices
        )


@contractor_bp.route("/list_contractors", methods=["GET"])
def list_contractors():
    # lon = request.args.get('lon')
    # lat = request.args.get('lat')
    # r = request.args.get('r')

    # TESTISIJAINTI
    address, content = "Hirvijärvi, Juupajoki", "Hakkuujäte"
    lon, lat, r = 24.566428395979575, 61.8578385779706, 300

    contractors = ContractorDivision(['name', 'address', 'latitude', 'longitude'])
    contractors.split_by_range(lat, lon, r)
    return render_template(
        "contractor_list.html",
        content=content,
        address=address,
        lat=lat,
        lon=lon,
        in_range=contractors.get_optimal(),
        out_range=contractors.get_suboptimal(),
    )

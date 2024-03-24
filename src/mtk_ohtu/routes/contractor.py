import math
from flask import Blueprint, render_template, request, redirect, url_for, abort, session, flash
from geojson import Point, Feature, FeatureCollection

from ..database import db_contractors
from ..database.db_enums import CategoryType, BatchUnitsType, EcoCategoryType
from ..config import DATABASE_POOL
from ..logic import user as users
from ..logic import logistics
from ..database import db_cargo as db
from ..logic.contractor_division import ContractorDivision

contractor_bp = Blueprint("contractor_bp", __name__)


@contractor_bp.route("/addlogistics", methods=["GET", "POST"])
def add_logistics():
    if request.method == "GET":
        eco_categories = [e.value for e in EcoCategoryType]
        material_categories = [e.value for e in CategoryType]
        units = [e.value for e in BatchUnitsType]
        return render_template(
            "addlogistics.html", eco_categories=eco_categories, material_categories=material_categories, units=units
        )

    if request.method == "POST":
        user_id = users.user_id()
        service_type = request.form.get("serviceType")
        name = (
            request.form.get("fullName")
            if service_type == "private"
            else request.form.get("companyName")
        )
        business_id = (
            request.form.get("businessId") if service_type == "company" else None
        )
        contractor_id = logistics.add_contractor(user_id, name, business_id)

        address = request.form.get("address")
        postcode = request.form.get("postcode")
        city = request.form.get("city")
        telephone = request.form.get("telephone")
        email = request.form.get("email")
        radius_type = request.form.get("radiusType")
        radius = request.form.get("radius") if radius_type == "custom-limit" else -1
        description = request.form.get("description")
        contractor_location_id = logistics.add_contractor_location(
            contractor_id,
            address,
            postcode,
            city,
            telephone,
            email,
            radius,
            description,
        )

        eco_types = request.form.getlist("eco_types[]")
        print(eco_types)
        for type in eco_types:
            print(type)
            logistics.add_eco_type(
                contractor_id,
                type
            )

        categories = request.form.getlist("materials[]")
        for c in categories:
            price = request.form.get(c + "-price_per_hour")
            base_rate = request.form.get(c + "-base_rate")
            max_capacity = request.form.get(c + "-max_capacity")
            type = request.form.get("radiusType-" + c)
            radius = (
                request.form.get("radius-" + c) if type == "custom-limit-" + c else -1
            )
            unit = request.form.get(c + "-unit")
            can_process = request.form.get(c + "-can_process")
            material_description = request.form.get(c + "-description")

            logistics.add_cargo_capability(
                contractor_location_id,
                c,
                price,
                base_rate,
                max_capacity,
                radius,
                unit,
                can_process,
                material_description,
            )

        session["contractor_id"] = contractor_id
        return redirect(url_for("main.contractor_bp.contractor"))


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
        contractor_info = db_contractors.db_get_contractor(user_id, DATABASE_POOL)
        if not contractor_info:
            return redirect(url_for("main.contractor_bp.add_logistics"))

        locations_and_cargo_capability = logistics.get_locations_and_cargo_capability(
            contractor_info.id
        )
        return render_template(
            "contractor.html",
            contractor=contractor_info,
            locations=locations_and_cargo_capability,
        )


@contractor_bp.route("/list_contractors", methods=["GET"])
def list_contractors():
    """
    Rendering template marked as 'test'
    """
    # lon = request.args.get('lon')
    # lat = request.args.get('lat')
    # r = request.args.get('r')

    # TESTISIJAINTI
    address, content = "Hirvijärvi, Juupajoki", "Hakkuujäte"
    lon, lat, r = 24.566428395979575, 61.8578385779706, 300

    contractors = ContractorDivision(lat, lon)
    contractors.split_by_range(lat, lon)
    return render_template(
        "contractor_list.html",
        content=content,
        address=address,
        lat=lat,
        lon=lon,
        in_range=contractors.get_optimal(),
        out_range=contractors.get_suboptimal(),
    )

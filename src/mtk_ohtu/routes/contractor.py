import math
from flask import Blueprint, render_template, request, redirect, url_for
from geojson import Point, Feature, FeatureCollection
from ..database.db_enums import CategoryType
from ..config import DATABASE_POOL
from ..logic import user as users
from ..logic import logistics
from ..database import database as db


contractor_bp = Blueprint("contractor_bp", __name__)


@contractor_bp.route("/addlogistics", methods=["GET", "POST"])
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
        user_id = users.user_id()
        address = request.form.get("address")
        radius = request.form.get("radius")
        categories = request.form.getlist("materials[]")
        base_rates = request.form.getlist("base_rates[]")
        prices_per_hour = request.form.getlist("prices_per_hour[]")
        maximum_capacities = request.form.getlist("max_capacities[]")
        maximum_distances = request.form.getlist("max_distances[]")

        if logistics.addlogistics(
            service_type, 
            user_id, 
            name, 
            business_id, 
            address, 
            radius, 
            categories, 
            base_rates, 
            prices_per_hour, 
            maximum_capacities,
            maximum_distances
        ):
            return redirect(url_for('contractor_bp.confirmation', message='Logistics submitted successfully'))
        else:
            return redirect(url_for('contractor_bp.confirmation', message='An error occurred while submitting logistics'))


@contractor_bp.route("/confirmation")
def confirmation():
    message = request.args.get('message', 'Confirmation message not provided')
    return render_template("confirmation.html", message=message)


@contractor_bp.route("/contractors", methods=["GET"])
def get_contractors(x,y,r):
    contractors = db.get_contractors_by_euclidean(x, y, r, DATABASE_POOL)
    return render_template("contractor_list.html", x, y, contractors)


@contractor_bp.route("/contractor", methods=["GET"])
def contractor():
    if request.method == "GET":
        user_id = users.user_id()
        contractor_db = db.db_get_contractor(user_id, DATABASE_POOL)
        if not contractor_db:
            return redirect("/addlogistics")

        cargo_prices_db = db.db_get_cargo_prices(contractor_db[0], DATABASE_POOL)
        contractor = {
            "name": contractor_db[1],
            "business_id": contractor_db[2],
            "address": contractor_db[3],
            "delivery_radius": contractor_db[4],
        }

        cargo_prices = []
        for cargo in cargo_prices_db:
            cargo_dict = {
                "type": cargo[2].value,
                "price_per_km": cargo[3],
                "base_rate": cargo[4]
            }
            cargo_prices.append(cargo_dict)
        
        return render_template("contractor.html", contractor=contractor, cargo_prices=cargo_prices)


@contractor_bp.route("/list_contractors", methods=["GET"])
def list_contractors():
    
    # lon = request.args.get('lon')
    # lat = request.args.get('lat')
    # r = request.args.get('r')

    #TESTISIJAINTI
    address, content = 'Hirvijärvi, Juupajoki', 'Hakkuujäte'
    lat, lon, r = 61.8578385779706, 24.566428395979575, 500

    #results = db.db_get_contractors_by_euclidean(lat, lon, r*0.00902, r/(111.320 * math.cos(lat * math.pi /180)), DATABASE_POOL)
    results = db.db_get_logistics
    features = []
    for r in results:
        feature = Feature(
            geometry=Point((r[0], r[1])), 
            properties={"name": r[2], "address": r[3]}
            )        
        features.append(feature)
    contractors = FeatureCollection(features)
    return render_template("contractor_list.html",
                           content=content, address=address,  
                           lon=lon, lat=lat, 
                           contractors=contractors)

from flask import Blueprint, render_template, redirect, request, abort, flash, url_for
from flask_babel import _
from ..logic import logistics
from ..database.db_enums import FuelType


contractor_location_bp = Blueprint("contractor_location_bp", __name__)


@contractor_location_bp.route("/contractor/location/add", methods=["POST"])
def add():
    contractor_id = logistics.contractor_id()
    if contractor_id == 0:
        abort(403)

    address = request.form["address"]
    postcode = request.form["postcode"]
    city = request.form["city"]
    telephone = request.form["telephone"]
    email = request.form["email"]
    description = request.form.get("description")
    radius_type = request.form.get("radiusType")
    radius = request.form.get("radius") if radius_type == "custom-limit" else -1

    if not logistics.add_contractor_location(
        contractor_id, address, postcode, city, telephone, email, radius, description
    ):
        flash(_("error_occurred"))
        return redirect(url_for("main.contractor_bp.contractor"))

    fuel_types = request.form.getlist("fuel_types[]")
    for type in fuel_types:
        logistics.add_fuel_type(
            contractor_id,
            type
        )

    flash(_("new_location_added"))
    return redirect(url_for("main.contractor_bp.contractor"))


@contractor_location_bp.route("/contractor/location/modify", methods=["POST"])
def modify():
    contractor_id = logistics.contractor_id()
    if contractor_id == 0:
        abort(403)

    location_id = request.form["location_id"]
    if not logistics.check_asset_ownership("location", location_id, contractor_id):
        abort(403)

    address = request.form["address"]
    postcode = request.form["postcode"]
    city = request.form["city"]
    telephone = request.form["telephone"]
    email = request.form["email"]
    radius_type = request.form["radiusType"]
    description = request.form.get("description")
    radius = request.form["radius"] if radius_type == "custom-limit" else -1

    if not logistics.modify_contractor_location(
        location_id, address, postcode, city, telephone, email, radius, description
    ):
        flash(_("error_occurred"))
        return redirect(url_for("main.contractor_bp.contractor"))

    flash(_("changes_saved"))
    return redirect(url_for("main.contractor_bp.contractor"))


@contractor_location_bp.route("/contractor/location/remove", methods=["POST"])
def remove():
    contractor_id = logistics.contractor_id()
    if contractor_id == 0:
        abort(403)

    location_id = request.form["location_id"]
    if not logistics.check_asset_ownership("location", location_id, contractor_id):
        abort(403)

    if not logistics.remove_contractor_location(location_id):
        flash(_("error_occurred"))
        return redirect(url_for("main.contractor_bp.contractor"))

    flash(_("location_removed"))
    return redirect(url_for("main.contractor_bp.contractor"))

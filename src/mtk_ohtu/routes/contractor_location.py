from flask import Blueprint, redirect, request, abort, flash
from ..logic import logistics


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
    radius_type = request.form["radiusType"]
    description = request.form.get("description")
    radius = (
        request.form["radius"]
        if radius_type == "custom-limit"
        else -1
    )

    if not logistics.add_contractor_location(
        contractor_id,
        address,
        postcode,
        city,
        telephone,
        email,
        radius,
        description
    ):
        flash("An error occured. Please try again.")
        return redirect("/contractor")

    flash("New location added")
    return redirect("/contractor")


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
    radius = (
        request.form["radius"]
        if radius_type == "custom-limit"
        else -1
    )

    if not logistics.modify_contractor_location(
        location_id,
        address,
        postcode,
        city,
        telephone,
        email,
        radius,
        description
    ):
        flash("An error occured. Please try again.")
        return redirect("/contractor")

    flash("Changes saved")
    return redirect("/contractor")


@contractor_location_bp.route("/contractor/location/remove", methods=["POST"])
def remove():
    contractor_id = logistics.contractor_id()
    if contractor_id == 0:
        abort(403)

    location_id = request.form["location_id"]
    if not logistics.check_asset_ownership("location", location_id, contractor_id):
        abort(403)

    if not logistics.remove_contractor_location(location_id):
        flash("An error occured. Please try again.")
        return redirect("/contractor")

    flash("Location removed")
    return redirect("/contractor")

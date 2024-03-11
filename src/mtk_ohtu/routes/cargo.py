from flask import Blueprint, redirect, request, abort, flash
from ..logic import logistics

cargo_bp = Blueprint("cargo_bp", __name__)


@cargo_bp.route("/contractor/cargo/add", methods=["POST"])
def add():
    contractor_id = logistics.contractor_id()
    if contractor_id == 0:
        abort(403)

    contractor_location_id = request.form["location_id"]
    if not logistics.check_asset_ownership(
        "location", contractor_location_id, contractor_id
    ):
        abort(403)

    category = request.form["category"]
    base_rate = request.form["base_rate"]
    price_per_hour = request.form["price_per_hour"]
    max_capacity = request.form["max_capacity"]
    max_distance = request.form["max_distance"]
    unit = request.form["unit"]
    can_process = request.form["can_process"]
    description = request.form["description"]

    if not logistics.add_cargo_capability(
        contractor_location_id,
        category,
        base_rate,
        price_per_hour,
        max_capacity,
        max_distance,
        unit,
        can_process,
        description,
    ):
        flash("An error occured. Please try again.")
        return redirect("/contractor")

    flash("Material type added")
    return redirect("/contractor")


@cargo_bp.route("/contractor/cargo/remove", methods=["POST"])
def remove():
    contractor_id = logistics.contractor_id()
    if contractor_id == 0:
        abort(403)

    cargo_id = int(request.form["cargo_id"])
    if not logistics.check_asset_ownership("cargo", cargo_id, contractor_id):
        abort(403)

    if not logistics.remove_cargo_capability(contractor_id, cargo_id):
        flash("An error occured. Please try again.")
        return redirect("/contractor")

    flash("Material type removed")
    return redirect("/contractor")

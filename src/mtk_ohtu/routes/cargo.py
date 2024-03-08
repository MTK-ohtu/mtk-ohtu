from flask import Blueprint, redirect, request, abort, flash
from ..logic import logistics

cargo_bp = Blueprint("cargo_bp", __name__)

@cargo_bp.route("/contractor/cargo/remove", methods=["POST"])
def remove():
    contractor_id = logistics.contractor_id()
    if contractor_id == 0:
        abort(403)

    cargo_id = int(request.form["cargo_id"])
    if not logistics.remove_cargo_capability(contractor_id, cargo_id):
        flash("An error occured. Please try again.")
        return redirect("/contractor")

    flash("Material type removed")
    return redirect("/contractor")

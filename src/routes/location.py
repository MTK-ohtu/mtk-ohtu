import datetime
import logic.route_calculator as route_calculator
from flask import Blueprint, render_template, request
from logic.location import Location


location_bp = Blueprint("location_bp", __name__)


@location_bp.route("/distance", methods=["get", "post"])
def distance():
    if request.method == "GET":
        return render_template(
            "distance.html", start_location=(0, 0), end_location=(0, 0)
        )
    if request.method == "POST":
        address1 = Location(request.form["address1"])
        address2 = Location(request.form["address2"])
        qt = int(request.form["quantity"])
        route = route_calculator.Route(address1, address2)
        route.calculate_route()
        start_location = (route.location1.latitude, route.location1.longitude)
        end_location = (route.location2.latitude, route.location2.longitude)

        return render_template(
            "distance.html",
            distance=round(route.distance / 1000, 1),
            duration=str(datetime.timedelta(seconds=(round(route.duration)))),
            geodesic_distance=round(route.geodesic_distance() / 1000, 1),
            price=round(route.distance / 1000 * qt * 0.5, 2),
            start_location=start_location,
            end_location=end_location,
            route_geojson=route.geojson,
        )

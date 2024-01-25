from flask import Blueprint, render_template, request, redirect
import route_calculator
import datetime

controller = Blueprint("example", __name__)

@controller.route("/")
def index():
    return render_template("index.html")

@controller.route("/listings")
def listings():
    return render_template("listings.html")

@controller.route("/createpost")
def create_listing():
    return render_template("createpost.html")


@controller.route("/distance", methods=["get", "post"])
def distance():
    if request.method == "GET":
        return render_template("distance.html")
    if request.method == "POST":
        address1 = request.form["address1"]
        address2 = request.form["address2"]
        route = route_calculator.Route(address1, address2, "miko.paajanen@helsinki.fi")

        return render_template(
            "distance.html",
            distance=round(route.distance/1000,1), 
            duration=str(datetime.timedelta(seconds=(route.duration))).split(".")[0],
            geodesic_distance=round(route.geodesic_distance()/1000,1)
        )
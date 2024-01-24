from flask import Blueprint, render_template, request, redirect

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
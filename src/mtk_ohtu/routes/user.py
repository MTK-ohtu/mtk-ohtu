from ..logic import user as users
from flask import Blueprint, render_template, request, redirect


user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        if users.register(username, password, email):
            return redirect("/")
        else:
            return render_template(
                "register.html", message="Käyttäjätunnus on jo käytössä"
            )


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template(
                "login.html", message="Salasana tai käyttäjätunnus väärin"
            )


@user_bp.route("/logout")
def logout():
    users.logout()
    return redirect("/")

from ..logic import user as users
from flask import Blueprint, render_template, request, redirect, url_for


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
            return redirect(url_for('main.misc_bp.index'))
        else:
            return render_template(
                "register.html", message="Käyttäjätunnus tai sähköposti on jo käytössä"
            )


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect(url_for('main.misc_bp.index'))
        else:
            return render_template(
                "login.html", message="Salasana tai käyttäjätunnus väärin"
            )


@user_bp.route("/logout")
def logout():
    users.logout()
    return redirect(url_for('main.misc_bp.index'))
from flask import Blueprint, request, render_template, g, redirect, abort

misc_bp = Blueprint("misc_bp", __name__)

@misc_bp.route("/")
def index():
    return render_template("index.html")

@misc_bp.route("/change_language/<string:new_language>")
def change_language(new_language: str):
    old_path = request.args.get("old_path")
    split_path = old_path.split('/')
    p = "/" + "/".join([new_language] + split_path[2:])
    g.lang_code = new_language
    return redirect(p)

# A route that accepts all routes not accepted by others
# Needed due to languages; otherwise inputting an invalid address will lead to:
# /X  /en/X  /en/en/X  /en/en/en/X  /en/en/en/en/X  /en/en/en/en/X  etc...
# because there is no route that accepts it and therefore the language parameter is not caught. There needs to be a route to catch it.
@misc_bp.route("/<path:p>")
def fallback_errorhandler(p: str):
    return render_template("404.html")
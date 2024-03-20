from flask import Blueprint, request, render_template, g, redirect

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
from flask import g, current_app, Blueprint, request, redirect, abort
from flask_babel import Babel
import logging

def lang_def():
    logging.warning(request.endpoint)
    lang_code = g.get("lang_code", None)
    logging.warning(lang_code)
    if lang_code is None or lang_code not in current_app.config["LANGUAGES"]:
        g.lang_code = request.accept_languages.best_match(current_app.config["LANGUAGES"])
        logging.warning(g.lang_code)
        if g.lang_code is None:
            abort(404)
        return redirect("/" + g.lang_code + request.path)


main = Blueprint("main", __name__, url_prefix='/<lang_code>')
@main.url_defaults
def add_language_code(endpoint, values):
    values.setdefault("lang_code", g.lang_code)

@main.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop("lang_code")

@main.before_app_request
def ensure_lang():
    if request.endpoint != "static" and request.endpoint is None:
        return lang_def()
    elif request.endpoint != "static" and "api_bp" not in request.endpoint:
        return lang_def()

def get_locale():
    return g.lang_code

from flask import Flask, request, Blueprint, g, redirect
from flask_session import Session
from .routes.listing import listing_bp
from .routes.contractor import contractor_bp
from .routes.contractor_location import contractor_location_bp
from .routes.location import location_bp
from .routes.cargo import cargo_bp
from .routes.user import user_bp
from .routes.misc import misc_bp
from .api.routes import api_bp
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel

# for localisation

main = Blueprint("main", __name__, url_prefix='/<lang_code>')
@main.url_defaults
def add_language_code(endpoint, values):
    values.setdefault("lang_code", g.lang_code)

@main.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop("lang_code")

@main.before_app_request
def ensure_lang():
    if request.endpoint != "static":
        lang_code = g.get("lang_code", None)
        if lang_code is None or lang_code not in app.config["LANGUAGES"]:
            g.lang_code = request.accept_languages.best_match(app.config["LANGUAGES"])
            return redirect("/" + g.lang_code + request.path)

def create_app():
    app = Flask(__name__, static_url_path="/static")
    app.url_map.strict_slashes = False

    main.register_blueprint(misc_bp)
    main.register_blueprint(user_bp)
    main.register_blueprint(contractor_bp)
    main.register_blueprint(contractor_location_bp)
    main.register_blueprint(listing_bp)
    main.register_blueprint(location_bp)
    main.register_blueprint(cargo_bp)

    app.register_blueprint(main)
    app.register_blueprint(api_bp, url_prefix="/api")

    app.config.from_object("mtk_ohtu.config")
    Session(app)
    csrf = CSRFProtect(app)
    csrf.exempt(api_bp)

    return app

app = create_app()

def get_locale():
    return g.lang_code

babel = Babel(app, locale_selector=get_locale)
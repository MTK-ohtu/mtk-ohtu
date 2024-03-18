from flask import Flask, request
from flask_session import Session
from .routes.listing import listing_bp
from .routes.contractor import contractor_bp
from .routes.contractor_location import contractor_location_bp
from .routes.location import location_bp
from .routes.cargo import cargo_bp
from .routes.user import user_bp
from .api.routes import api_bp
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel

def create_app():
    app = Flask(__name__, static_url_path="/static")

    app.register_blueprint(user_bp)
    app.register_blueprint(contractor_bp)
    app.register_blueprint(contractor_location_bp)
    app.register_blueprint(listing_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(cargo_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    app.config.from_object("mtk_ohtu.config")
    Session(app)
    csrf = CSRFProtect(app)
    csrf.exempt(api_bp)

    return app

def get_locale():
    return request.accept_languages.best_match(app.config["LANGUAGES"])

app = create_app()

babel = Babel(app, locale_selector=get_locale)
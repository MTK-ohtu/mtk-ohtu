from flask import Flask
from flask_session import Session
from .config import SECRET_KEY
from .routes.listing import listing_bp
from .routes.contractor import contractor_bp
from .routes.contractor_location import contractor_location_bp
from .routes.location import location_bp
from .routes.cargo import cargo_bp
from .routes.user import user_bp
from .api.routes import api_bp
from flask_wtf.csrf import CSRFProtect


def create_app():
    app = Flask(__name__, static_url_path="/static")
    app.secret_key = SECRET_KEY

    app.register_blueprint(user_bp)
    app.register_blueprint(contractor_bp)
    app.register_blueprint(contractor_location_bp)
    app.register_blueprint(listing_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(cargo_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    app.config.from_object(__name__)
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    csrf = CSRFProtect(app)
    csrf.exempt(api_bp)

    return app


app = create_app()

from flask import Flask
from flask_session import Session
from .config import SECRET_KEY
from .routes.listing import listing_bp
from .routes.contractor import contractor_bp
from .routes.location import location_bp
from .routes.user import user_bp
from .api.routes import api_bp


def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.secret_key = SECRET_KEY

    app.register_blueprint(user_bp)
    app.register_blueprint(contractor_bp)
    app.register_blueprint(listing_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    app.config.from_object(__name__)
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    return app


app = create_app()

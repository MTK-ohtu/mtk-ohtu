from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel
from flask import Flask
from flask_session import Session
from .routes.listing import listing_bp
from .routes.contractor import contractor_bp
from .routes.contractor_location import contractor_location_bp
from .routes.location import location_bp
from .routes.cargo import cargo_bp
from .routes.user import user_bp
from .routes.misc import misc_bp
from .api.routes import api_bp
from .lang import main, get_locale

IS_REGISTERED = False

def register_blueprints_to_main():
    global IS_REGISTERED
    if not IS_REGISTERED:
        main.register_blueprint(misc_bp)
        main.register_blueprint(user_bp)
        main.register_blueprint(contractor_bp)
        main.register_blueprint(contractor_location_bp)
        main.register_blueprint(listing_bp)
        main.register_blueprint(location_bp)
        main.register_blueprint(cargo_bp)
        IS_REGISTERED = True


def create_app():
    app = Flask(__name__, static_url_path="/static")
    app.url_map.strict_slashes = False
    register_blueprints_to_main()
    app.register_blueprint(main)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.config.from_object("mtk_ohtu.config")
    Session(app)
    csrf = CSRFProtect(app)
    csrf.exempt(api_bp)
    Babel(app, locale_selector=get_locale)

    return app


app = create_app()

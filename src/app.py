from config import SECRET_KEY
from flask import Flask
from flask_session import Session
from controllers.routes import controller


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    app.register_blueprint(controller)

    app.config.from_object(__name__)
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    return app


app = create_app()

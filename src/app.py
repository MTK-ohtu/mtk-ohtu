from config import SECRET_KEY
from flask import Flask
from controllers.example_controller import test_controller

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    app.register_blueprint(test_controller)

    return app

app = create_app()

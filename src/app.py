# from config import SECRET_KEY
from flask import Flask
from controllers.routes import controller
from database.database import db_excecute_file
from config import DATABASE_CONFIG


def create_app():
    app = Flask(__name__)
    # app.secret_key = SECRET_KEY
    db_excecute_file("schema.sql", DATABASE_CONFIG)
    db_excecute_file("db_mock_data.sql", DATABASE_CONFIG)
    app.register_blueprint(controller)

    return app


app = create_app()

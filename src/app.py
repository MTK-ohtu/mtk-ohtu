# from config import SECRET_KEY
from flask import Flask, session
from controllers.routes import controller


def create_app():
    app = Flask(__name__)
    # app.secret_key = SECRET_KEY
<<<<<<< HEAD
    
    db_excecute_file("schema.sql", DATABASE_CONFIG)
    db_excecute_file("db_mock_data.sql", DATABASE_CONFIG)
=======

>>>>>>> 94310df0d0dae80d528912012e687936499b3a25
    app.register_blueprint(controller)

    return app


app = create_app()

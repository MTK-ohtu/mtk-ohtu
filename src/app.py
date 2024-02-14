<<<<<<< HEAD
from config import SECRET_KEY
from flask import Flask
=======
# from config import SECRET_KEY
from flask import Flask, session
>>>>>>> main
from controllers.routes import controller


def create_app():
    app = Flask(__name__)
<<<<<<< HEAD
    app.secret_key = SECRET_KEY

=======
    # app.secret_key = SECRET_KEY
>>>>>>> main
    app.register_blueprint(controller)

    return app


app = create_app()

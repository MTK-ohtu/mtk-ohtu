from flask import Blueprint

test_controller = Blueprint("example", __name__)

@test_controller.route("/")
def index():
    return "Hello world!"


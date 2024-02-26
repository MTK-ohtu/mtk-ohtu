from marshmallow import ValidationError
from ..database.db_datastructs import Listing
from ..logic.location import Location
from flask import Blueprint, request
from ..api.logistics_info_schema import LogisticsInfoSchema
from ..logic.logistics_info import get_logistics_info
from ..routes.listing import get_url_for_listing

api_bp = Blueprint("api_bp", __name__)


@api_bp.route("/logistics_info", methods=["GET"])
def logistics_info():
    """API3 implementation.
    Excepts the mimetype of the GET request to be application/json.

    The json body should have the form:
        {
            "listing": (int) the ID of the listing,
            "location": (str) the address of user
        }

    Returns json in the following form:
        {
            "distance": (float) the distance in kilometers from the supplied location to the listing,
            "num_providers": (int) the number of available logistics providers,
            "link": (str) a full (not relative) URL leading to the logistics page providing more info
        }
    """

    try:
        listing, location = LogisticsInfoSchema().load(request.get_json())
    except ValidationError as err:
        return err.messages, 422

    distance, num_providers = get_logistics_info(listing, location)

    return {
        "distance": distance,
        "num_providers": num_providers,
        "link": get_url_for_listing(listing),
    }

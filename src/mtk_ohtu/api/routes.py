from marshmallow import ValidationError
from flask import Blueprint, request
from ..api.logistics_info_schema import LogisticsInfoSchema
from ..api.posting_api_schema import PostingApiSchema, EntryType
from ..logic.logistics_info import get_logistics_info
from ..routes.listing import get_url_for_listing
from ..database.db_api import db_get_api_key
from ..database.db_datastructs import APIKey
from ..database.db_listings import db_create_new_listing_from_api_response, db_update_listing_from_api_response
from ..config import DATABASE_POOL

api_bp = Blueprint("api_bp", __name__)


@api_bp.route("/logistics_info", methods=["POST"])
def logistics_info():
    """API3 implementation.
    Expects the mimetype of the POST request to be application/json.
    Expects the API key to be supplied in the headers as 'API-Key'.

    The json body should have the form:
        {
            "user_id": (int) the ID of the kiertoasuomesta user,
            "posting_id": (int) the ID of the listing,
            "address": {
                "country": (str, optional),
                "city": (str, optional),
                "state": (str, optional),
                "streetAddress": (str, either this OR latitude & longitude specified),
                "postalCode": (str, optional),
                "apartment": (str, optional),
                "latitude": (float, either this & longitude OR streetAddress provided)
                "longitude": (float, either this & latitude OR streetAddress provided)
            }
        }

    Returns json in the following form:
        {
            "success": (bool),
            "message": (str) error or success message,

    - if successful, the following attributes are supplied -

            "distance": (float) the distance in kilometers from the supplied location to the listing,
            "provider_count": (int) the number of available logistics providers,
            "logistics_url": (str) a full (not relative) URL leading to the logistics page providing more info
        }

    Error codes:
        401: API-Key is incorrect
        400: JSON request is malformed (for example due to missing fields, extra fields, etc.) or params are otherwise incorrect
        404: incorrect URL
        500: other errors
    """

    api_success, api_msg, api_key = validate_api_key()
    if not api_success:
        return {"success": False, "message": api_msg}, 401

    try:
        data = LogisticsInfoSchema().load(request.get_json())
    except ValidationError as err:
        return {"success": False, "message": err.messages}, 400

    listing = data["posting_id"]
    location = data["address"][1]

    distance, num_providers = get_logistics_info(listing, location)

    return {
        "distance": distance,
        "provider_count": num_providers,
        "logistics_url": get_url_for_listing(listing),
    }


@api_bp.route("/postings", methods=["POST"])
def postings():
    """API2 implementation.
    Expects the mimetype of the POST request to be application/json.
    Expects the API key to be supplied in the headers as 'API-Key'.

    The json body should have the form:
        {
            "posting_id": (int)
            "entry_type": (create/update/delete)
            "title": (string, update/delete: optional)
            "description": (string, optional)
            "category": (CategoryType, update/delete: optional)
            "sub_category": (string, update/delete: optional)
            "post_type": (BuyOrSell, update/delete: optional)
            "delivery_method": (DeiveryType, update/delete: optional)
            "demand": (SupplyDemandType, update/delete: optional)
            "expiry_date": (timestamp, update/delete: optional)
            "price": (float, update/delete: optional)
            "delivery_details": (string, optional)
            "address": (Address, update/delete: optional)
            "date_created": (timestamp, update/delete: optional)
        }

    Returns json in the following form:
        {
            "success": (bool),
            "message": (str) error or success message
        }

    Error codes:
        401: API-Key is incorrect
        400: JSON request is malformed (for example due to missing fields, extra fields, etc.)
        404: resource not found (update, delete)
        500: other errors
    """
    try:
        data = PostingApiSchema().load(request.get_json())
    except ValidationError as err:
        return {"success": False, "message": err.messages}, 400

    match data[0]:
        case EntryType.CREATE:
            try:
                db_create_new_listing_from_api_response(data[1], DATABASE_POOL)
            except Exception as err:
                return {"success": False, "message": err}, 401

        case EntryType.UPDATE:
            try:
                db_update_listing_from_api_response(data[1], DATABASE_POOL)
            except Exception as err:
                return {"success": False, "message": err}, 404

        case EntryType.DELETE:
            print(data)

        case _:
            raise ValueError

    return {
        "success": True,
    }, 200


def validate_api_key() -> tuple[bool, str, APIKey]:
    """Checks if the API key in the request headers is correct.

    Returns:
        tuple[success (bool), message (str), APIKey]
    """

    api_key_str = request.headers.get("API-Key", None)
    if api_key_str is None:
        return (False, "No API-Key header field specified.", None)

    api_key = db_get_api_key(api_key_str, DATABASE_POOL)
    if api_key is None:
        return (False, "Provided API-Key is invalid.", None)

    return (True, "", api_key)

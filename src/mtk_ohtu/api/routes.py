from marshmallow import ValidationError
from ..database.db_listings import db_get_product_by_id
from ..logic.location import Location
from flask import Blueprint, request
from ..api.logistics_info_schema import LogisticsInfoSchema
from ..api.posting_api_schema import PostingApiSchema, EntryType
from ..logic.logistics_info import get_logistics_info
from ..routes.listing import get_url_for_listing
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
        400: JSON request is malformed (for example due to missing fields, extra fields, etc.)
        404: either the user_id, posting_id or the address are not found
        500: other errors
    """

    try:
        data = LogisticsInfoSchema().load(request.get_json())
    except ValidationError as err:
        return {"success": False, "message": err.messages}, 400
    
    listing = db_get_product_by_id(data["posting_id"], DATABASE_POOL)
    if listing is None:
        return {"success": False, "message": "Listing not found"}, 404
    
    location = None
    address = data["address"]
    if "latitude" in address and "longitude" in address:
        location = Location((address["longitude"], address["latitude"]))
    else:
        try:
            location = Location(address["streetAddress"])
        except ValueError as err:
            return {"success": False, "message": err.args}, 404


    distance, num_providers = get_logistics_info(listing, location)

    return {
        "distance": distance,
        "provider_count": num_providers,
        "logistics_url": get_url_for_listing(listing),
    }

@api_bp.route("/postings", methods=["POST"])
def posting_edit_api():
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
        404: either the user_id, posting_id or the address are not found
        500: other errors
    """

    try:
        data = PostingApiSchema().load(request.get_json())
    except ValidationError as err:
        return {"success": False, "message": err.messages}, 400
    
    match data[0]:
        case EntryType.CREATE:
            print(data)
        
        case EntryType.UPDATE:
            print(data)
        
        case EntryType.DELETE:
            print(data)
        
        case _:
            raise ValueError
    
    return {"success": True}, 200

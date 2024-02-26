from marshmallow import Schema, post_load, fields, ValidationError
from ..logic.location import Location
from ..database.db_datastructs import Listing
from ..api.class_field import ClassField
from ..database.db_listings import db_get_product_by_id
from ..config import DATABASE_POOL


class LogisticsInfoSchema(Schema):
    """A Marshmallow schema for the API3 endpoint (getting logistics info when provided a listing ID and a user's location)"""

    listing = fields.Method(deserialize="deserialize_listing", required=True)
    location = ClassField(Location, required=True)

    def deserialize_listing(self, id):
        if type(id) != int:
            raise ValidationError("Invalid listing id (int expected)")

        Listing = db_get_product_by_id(id, DATABASE_POOL)
        if Listing is None:
            raise ValidationError(f"Invalid listing id (no listing found with id {id})")

        return Listing

    @post_load
    def make(self, data, **kwargs) -> tuple[Listing, Location]:
        """Returns a tuple: (the Listing object, the Location object)"""
        return (data["listing"], data["location"])

from marshmallow import Schema, fields, ValidationError
from mtk_ohtu.api.address_schema import AddressSchema
from ..database.db_listings import db_get_product_by_id
from ..config import DATABASE_POOL


class LogisticsInfoSchema(Schema):
    """A Marshmallow schema for the API3 endpoint"""

    user_id = fields.Int(required=False)
    posting_id = fields.Method(deserialize="deserialize_posting_id", required=True)
    address = fields.Nested(AddressSchema, required=True)

    def deserialize_posting_id(self, id):
        if type(id) != int:
            raise ValidationError("Invalid posting_id (int expected)")

        listing = db_get_product_by_id(id, DATABASE_POOL)
        if listing == None:
            raise ValidationError("Listing not found")

        return listing

from marshmallow import Schema, fields
from mtk_ohtu.api.address_schema import AddressSchema

class LogisticsInfoSchema(Schema):
    """A Marshmallow schema for the API3 endpoint"""

    user_id = fields.Int(required=False)
    posting_id = fields.Int(required=True)
    address = fields.Nested(AddressSchema, required=True)
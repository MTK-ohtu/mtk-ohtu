from enum import Enum
from marshmallow import Schema, post_load, fields, ValidationError
from ..database.db_enums import BuyOrSell, DeliveryMethodType, SupplyDemandType


class EntryType(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class posting_api_schema(Schema):
    posting_id = fields.Int(required=True)
    entry_type = fields.Enum(EntryType, required=True)
    title = fields.Str()
    description = fields.Str()
    category = fields.Str()
    sub_category = fields.Str()
    post_type = fields.Enum(BuyOrSell)
    delivery_method = fields.Enum(DeliveryMethodType)
    demand = fields.Enum(SupplyDemandType)
    expiry_date = fields.DateTime()
    price = fields.Float()
    delivery_details = fields.Str()
    address = 2 # (required): address object
    date_created = fields.DateTime()

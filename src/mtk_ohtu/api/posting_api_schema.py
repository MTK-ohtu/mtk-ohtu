from enum import Enum
from marshmallow import Schema, post_load, fields, ValidationError
from .class_field import ClassField
from .address_datatype import Address
from ..database.db_enums import BuyOrSell, DeliveryMethodType, SupplyDemandType


class EntryType(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class PostingApiSchema(Schema):
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
    address = ClassField(Address)
    date_created = fields.DateTime()

    @post_load
    def j():
        pass
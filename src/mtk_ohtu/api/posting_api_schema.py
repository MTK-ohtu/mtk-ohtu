from enum import Enum
from marshmallow import Schema, post_load, validates_schema, fields, ValidationError
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

    create_requirements = ["title", 
                           "category", 
                           "sub_category", 
                           "post_type", 
                           "delivery_method", 
                           "demand", 
                           "expiry_date", 
                           "price", 
                           "address", 
                           "date_created"]

    @validates_schema
    def validate_create(self, data):
        if data["entry_type"] == EntryType.CREATE:
            if not all({k: data[k] for k in data if k in self.create_requirements}):
                raise ValidationError("Missing required fields from create")

    @post_load
    def make_posting(self, data):
        pass
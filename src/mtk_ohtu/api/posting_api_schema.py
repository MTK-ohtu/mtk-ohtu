from enum import Enum
from marshmallow import Schema, post_load, validates_schema, fields, ValidationError
from .address_schema import AddressSchema
from ..database.db_enums import (
    BuyOrSell,
    DeliveryMethodType,
    SupplyDemandType,
    CategoryType,
)
from ..database.db_datastructs import FullListing
from ..logic.location import Location


class EntryType(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class PostingApiSchema(Schema):
    posting_id = fields.Int(required=True)
    entry_type = fields.Enum(EntryType, required=True, by_value=True)
    title = fields.Str()
    description = fields.Str()
    category = fields.Enum(CategoryType, by_value=True)
    sub_category = fields.Str()
    post_type = fields.Enum(BuyOrSell, by_value=True)
    delivery_method = fields.Enum(DeliveryMethodType, by_value=True)
    demand = fields.Enum(SupplyDemandType, by_value=True)
    expiry_date = fields.Int()
    price = fields.Float()
    delivery_details = fields.Str()
    address = fields.Nested(AddressSchema)
    date_created = fields.Int()

    create_requirements = [
        "title",
        "category",
        "sub_category",
        "post_type",
        "delivery_method",
        "demand",
        "expiry_date",
        "price",
        "address",
        "date_created",
    ]

    @validates_schema
    def validate_create(self, data, **kwargs):
        if data["entry_type"] == EntryType.CREATE:
            if not all({k: data[k] for k in data if k in self.create_requirements}):
                raise ValidationError("Missing required fields from create")

    @post_load
    def make_posting(self, data, **kwargs):
        entry = data.pop("entry_type")
        if "address" in data:
            address = data.pop("address")
            data["location"] = address[1]
            data["address"] = address[0]
        return (entry, FullListing(**data))

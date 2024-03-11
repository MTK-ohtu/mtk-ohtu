from marshmallow import Schema, fields, post_load, ValidationError
from ..logic.location import Location


class AddressSchema(Schema):
    """Either a fully supplied latitude & longitude pair, OR a streetAddress is expected."""

    latitude = fields.Float()
    longitude = fields.Float()

    country = fields.Str()
    city = fields.Str()
    state = fields.Str(allow_none=True)
    streetAddress = fields.Str()
    postalCode = fields.Str(allow_none=True)
    apartment = fields.Str(allow_none=True)

    @post_load
    def v(self, data, **kwargs):
        if "latitude" in data and "longitude" in data:
            return Location(data["latitude"], data["longitude"])

        if "streetAddress" in data:
            try:
                loc = Location(data["streetAddress"])
                return loc
            except ValueError as err:
                raise ValidationError({"streetAddress": err.args})

        raise ValidationError(
            "Either a full latitude & longitude pair, OR a streetAddress is expected."
        )

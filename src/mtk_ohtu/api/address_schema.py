from marshmallow import Schema, fields, validates_schema, ValidationError


class AddressSchema(Schema):
    '''Either a fully supplied latitude & longitude pair, OR a streetAddress is expected.
    '''
    latitude    = fields.Float()
    longitude   = fields.Float()

    country     = fields.Str()
    city        = fields.Str()
    state       = fields.Str()
    streetAddress = fields.Str()
    postalCode  = fields.Str()
    apartment   = fields.Str()

    @validates_schema
    def v(self, data, **kwargs):
        if "latitude" in data and "longitude" in data:
            return
        if "streetAddress" in data:
            return

        raise ValidationError("Either a full latitude & longitude pair, OR a streetAddress is expected.")
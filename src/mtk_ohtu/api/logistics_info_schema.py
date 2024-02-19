from marshmallow import Schema, post_load
from ..logic.location import Location
from ..logic.listing import Listing
from ..api.class_field import ClassField

class LogisticsInfoSchema(Schema):
    '''A Marshmallow schema for the API3 endpoint (getting logistics info when provided a listing ID and a user's location)
    '''

    listing = ClassField(Listing, required=True)
    location = ClassField(Location, required=True)

    @post_load
    def make(self, data, **kwargs) -> tuple[Listing, Location]:
        '''Returns a tuple: (the Listing object, the Location object)
        '''
        return (data["listing"], data["location"])
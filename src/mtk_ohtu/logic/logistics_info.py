from ..logic.listing import Listing
from ..logic.location import Location

def get_logistics_info(listing: Listing, location: Location) -> tuple[float, int]:
    '''Gets the necessary logistics info for API3 when supplied the listing and the location of the user.

    Args:
        listing (Listing): the listing / posting / item / sidestream source / etc. in question,
        location (Location): the location of the user, according to which to calculate the 
    
    Returns:
        a tuple: (float: the distance from the listing to the user, int: the number of available logistics providers)
    '''

    return (0.0, 123)
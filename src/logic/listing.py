from config import DATABASE_POOL
from database.database import db_get_product_by_id
from logic.location import Location

class Listing:
    """A class for storing listings.
    
    Attributes:
        id: (integer),
        name: (str),
        price (float),
        address (str),
        description (str),
        seller_name (str),
        location (Location)
    """

    def __init__(self, id: int):
        if type(id) != int:
            raise ValueError("Invalid listing id (int expected)")
        
        self.id = id
        info = db_get_product_by_id(id, DATABASE_POOL)
        if info is None:
            raise ValueError(f"Invalid listing id (no listing found with id {id})")
        
        self.name, self.price, self.address, self.description, self.seller_name, long, lat = info
        self.location = Location((long, lat))
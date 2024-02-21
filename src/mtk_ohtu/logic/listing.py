from dataclasses import dataclass
from ..config import DATABASE_POOL
from ..logic.location import Location
from ..database.db_enums import CategoryType

@dataclass
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
    id: int
    category: CategoryType
    price: float
    address: str
    description: str
    seller: str
    location: Location
from dataclasses import dataclass
from ..logic.location import Location


@dataclass
class LogisticsNode:
    id: int
    user_id: int
    name: str
    business_id: str
    address: str
    location: Location
    delivery_radius: float  # in kilometers

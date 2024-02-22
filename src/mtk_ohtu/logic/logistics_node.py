from dataclasses import dataclass
from ..logic.location import Location


@dataclass
class LogisticsNode:
    id: int
    contractor_id: int
    address: str
    name: str
    location: Location
    delivery_radius: int

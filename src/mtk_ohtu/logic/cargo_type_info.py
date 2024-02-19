from dataclasses import dataclass
from ..database.db_enums import CategoryType

@dataclass
class CargoTypeInfo:
    logistics_id: int
    type: CategoryType
    price_per_km: int
    base_rate: int
    max_capacity: int
    max_distance: int
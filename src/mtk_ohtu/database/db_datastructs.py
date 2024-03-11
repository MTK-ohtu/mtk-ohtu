from dataclasses import dataclass
from mtk_ohtu.database.db_enums import CategoryType, BatchUnitsType, BuyOrSell, DeliveryMethodType, SupplyDemandType
from mtk_ohtu.logic.location import Location

@dataclass(kw_only=True)
class FullListing:
    """A class for storing the full listing row
    """
    posting_id: int
    title: str
    category: CategoryType
    sub_category: str
    post_type: BuyOrSell
    delivery_method: DeliveryMethodType
    demand: SupplyDemandType
    expiry_date: int
    price: float
    delivery_details: str
    address: str
    description: str
    location: Location
    date_created: int


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


@dataclass
class CargoTypeInfo:
    id: int
    contractor_location_id: int
    type: CategoryType
    price_per_km: int
    base_rate: int
    max_capacity: int
    max_distance: int
    unit: BatchUnitsType
    can_process: bool
    description: str


@dataclass
class LogisticsContractor:
    """
    A class for storing contractor information
    """

    id: int
    user_id: int
    name: str
    business_id: str


@dataclass
class LogisticsNode:
    id: int
    contractor_id: int
    address: str
    name: str
    location: Location
    delivery_radius: int

@dataclass
class APIKey:
    id: int
    name: str
    key: str
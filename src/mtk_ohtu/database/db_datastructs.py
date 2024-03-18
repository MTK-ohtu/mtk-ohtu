from dataclasses import dataclass, asdict
from mtk_ohtu.database.db_enums import (
    CategoryType,
    BatchUnitsType,
    BuyOrSell,
    DeliveryMethodType,
    SupplyDemandType,
    SubcategoryType,
)
from mtk_ohtu.logic.location import Location


LISTING_NAME_TABLE = {
    "posting_id": "id",
    # None: "user_id"
    "title": "title",
    "category": "category",
    "sub_category": "subcategory",
    "post_type": "listing_type",
    "delivery_method": "delivery_method",
    # None: "continuous"
    "demand": "supply_demand",
    "expiry_date": "expiration_date",
    "batch_size": "batch_size",
    "batch_type": "batch_type",
    # None: "image"
    "price": "price",
    "delivery_details": "delivery_details",
    "address": "address",
    "description": "description",
    "date_created": "date_created",
    "location": "location"
    # None: "complies_with_regulations"
}

@dataclass(kw_only=True)
class FullListing:
    """A class for storing the full listing row for api creation, or updates"""

    posting_id: int
    title: str = None
    category: CategoryType = None
    sub_category: SubcategoryType = None
    post_type: BuyOrSell = None
    delivery_method: DeliveryMethodType = None
    demand: SupplyDemandType = None
    expiry_date: int = None
    batch_size: int = None
    batch_type: BatchUnitsType = None
    price: float = None
    delivery_details: str = None
    address: str = None
    description: str = None
    location: Location = None
    date_created: int = None

    def update_dict(self):
        return {LISTING_NAME_TABLE[k] : v for k,v in asdict(self).items()
                if LISTING_NAME_TABLE[k] is not None and v is not None}


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
    category: CategoryType
    subcategory: SubcategoryType
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


@dataclass
class LocationService:
    """
    Describes one location related service.
    For now, location can have multiple services
    for same cargo type (CategoryType).
    Are used in ContractorDivision to create lists 
    for frontend.
    """
    contractor_id: int
    contractor_location_id: int
    name: str
    address: str
    telephone: str
    email: str
    location: Location
    type: CategoryType
    price_per_km: int
    base_rate: int
    max_capacity: int
    max_distance: int
    delivery_radius: int
    unit: BatchUnitsType
    can_process: bool
    description: str




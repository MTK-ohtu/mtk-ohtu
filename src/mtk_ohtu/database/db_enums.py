from enum import Enum


class BuyOrSell(Enum):
    BUY = "buy"
    SELL = "sell"


class DeliveryMethodType(Enum):
    PICKUP = "pickup"
    SELLER_DELIVERS = "seller delivers"
    FREIGHT = "freight"


class SupplyDemandType(Enum):
    ONE_TIME = "one time"
    RECURRING = "recurring"
    ANUALLY = "annually"
    WEEKLY = "weekly"


class BatchUnitsType(Enum):
    TN = "tn"
    M3 = "m3"
    KG = "kg"
    L = "l"
    PCS = "pcs"
    BATCH = "batch"


class VehicleRequirementType(Enum):
    DRY = "dry"
    REFRIGERATED = "refrigerated"
    TANKER = "tanker"
    FLATBED = "flatbed"
    CONTAINER = "container"


class CategoryType(Enum):
    DRY_MANURE = "Dry manure"
    SLUDGE_MANURE = "Sludge manure"
    SEPARATED_MANURE = "Separated manure"
    OTHER_MANURE = "Other manure"
    GRASS_WASTE_FODDER_AND_GREEN_GROWTHS = "Grass, waste fodder and green growths"
    BASKET_FODDER = "Basket fodder"
    PLANT_BASED_BIOMASSES = "Plant-based biomasses"
    ANIMAL_BASED_BIOMASSES = "Animal-based biomasses"
    SOIL_AND_GROWING_MEDIA = "Soil and growing media"
    DIGESTION = "Digestion"
    WOOD_FOREST_BIOMASS = "Wood (forest biomass)"
    WOOD_TREATED_WOOD = "Wood (treated wood)"
    OTHER_SIDE_STREAMS_NOT_BIOMASS = "Other side streams (not biomass)"


DEFINED_ENUMS = {
    "buying_or_selling": BuyOrSell,
    "delivery_method_type": DeliveryMethodType,
    "supply_demand_type": SupplyDemandType,
    "batch_units_type": BatchUnitsType,
    "category_type": CategoryType,
    "vehichle_requirement_type": VehicleRequirementType,
}

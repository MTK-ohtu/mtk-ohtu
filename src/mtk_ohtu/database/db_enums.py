from enum import Enum

def _(str):
    return str

class BuyOrSell(Enum):
    BUY = _("buy")
    SELL = _("sell")


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
    TN = _("tn")
    M3 = _("m3")
    KG = _("kg")
    L = _("l")
    PCS = _("pcs")
    BATCH = _("batch")


class VehicleRequirementType(Enum):
    DRY = "dry"
    REFRIGERATED = "refrigerated"
    TANKER = "tanker"
    FLATBED = "flatbed"
    CONTAINER = "container"


class CategoryType(Enum):
    MANURE = _("Manure")
    GRASS_WASTE_FODDER_AND_GREEN_GROWTHS = _("Grass, waste fodder and green growths")
    BASKET_FODDER = _("Basket fodder")
    PLANT_BASED_BIOMASSES = _("Plant-based biomasses")
    ANIMAL_BASED_BIOMASSES = _("Animal-based biomasses")
    SOIL_AND_GROWING_MEDIA = _("Soil and growing media")
    DIGESTION = _("Digestion")
    WOOD = _("Wood")
    OTHER_SIDE_STREAMS_NOT_BIOMASS = _("Other side streams (not biomass)")
    LOGISTICS_AND_CONTRACTING = _("Logistics and contracting")

class SubcategoryType(Enum):
    DRY_MANURE = _("Dry manure")
    SLUDGE_MANURE = _("Sludge manure")
    SEPARATED_MANURE = _("Separated manure")
    OTHER_MANURE = _("Other manure")
    FOREST_BIOMASS = _("Forest biomass")
    TREATED_WOOD = _("Treated wood")


class EcoCategoryType(Enum):
    ELECTRICITY = _("electricity")
    BIOGAS = _("biogas")
    BIODIESEL = _("biodiesel")
    HYDROGEN = _("hydrogen")


DEFINED_ENUMS = {
    "buying_or_selling": BuyOrSell,
    "delivery_method_type": DeliveryMethodType,
    "supply_demand_type": SupplyDemandType,
    "batch_units_type": BatchUnitsType,
    "category_type": CategoryType,
    "vehichle_requirement_type": VehicleRequirementType,
    "eco_category_type": EcoCategoryType,
    "subcategory_type": SubcategoryType
}

from enum import Enum, auto

class BuyOrSell(Enum):
    BUY = 'buy'
    SELL = 'sell'

class DeliveryMethodType(Enum):
    PICKUP = 'pickup'
    SELLER_DELIVERS = 'seller delivers'
    FREIGHT = 'freight'


class SupplyDemandType(Enum):
    ONE_TIME='one time'
    RECURRING = 'recurring'
    ANUALLY = 'annually'
    WEEKLY = 'weekly'

#CREATE TYPE batch_units_type AS ENUM ('tn', 'm3', 'kg', 'l', 'pcs', 'batch');

 #   CREATE TYPE vehichle_requirement_type AS ENUM ('dry', 'refrigerated', 'tanker', 'flatbed', 'container');

class CategoryType(Enum):
    MANURE = 'Manure' 
    GRASS_WASTE_FODDER_AND_GREEN_GROWTHS = 'Grass, waste fodder and green growths' 
    BASKET_FODDER = 'Basket fodder' 
    PLANT_BASED_BIOMASSES = 'Plant-based biomasses' 
    ANIMAL_BASED_BIOMASSES = 'Animal-based biomasses' 
    SOIL_AND_GROWING_MEDIA = 'Soil and growing media' 
    DIGESTION = 'Digestion' 
    WOOD = 'Wood' 
    OTHER_SIDE_STREAMS_NOT_BIOMASS = 'Other side streams (not biomass)' 
    LOGISTICS_AND_CONTRACTING = 'Logistics and contracting' 
    OTHER = 'Other'



DEFINED_ENUMS = {
    "buying_or_selling" : BuyOrSell,
    "delivery_method_type": DeliveryMethodType,
    "supply_demand_type": SupplyDemandType,
    "category_type": CategoryType
}
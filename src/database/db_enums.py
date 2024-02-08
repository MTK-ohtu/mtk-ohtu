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


DEFINED_ENUMS = {
    "buying_or_selling" : BuyOrSell,
    "delivery_method_type": DeliveryMethodType,
    "supply_demand_type": SupplyDemandType
}
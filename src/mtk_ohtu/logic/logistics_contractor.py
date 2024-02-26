from dataclasses import dataclass


@dataclass
class LogisticsContractor:
    """
    A class for storing contractor information
    """
    id: int
    user_id: int
    name: str
    business_id: str
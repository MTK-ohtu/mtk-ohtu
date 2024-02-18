
class Listing:
    """A class for storing listings.
    
    Attributes:
        id: (integer)
    """

    def __init__(self, id: int):
        if type(id) != int:
            raise ValueError("Invalid listing id (int expected)")
        
        self.id = id
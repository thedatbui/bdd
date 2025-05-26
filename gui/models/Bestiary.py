class Bestiary:
    """
    Model representing a Monster in the Bestiary.

    Attributes:
        id (int): Unique identifier of the monster.
        name (str): Name of the monster.
        lifePoints (int): Number of life points (PV) of the monster.
    """
    def __init__(self, id: int, name: str, lifePoints: int):
        self.id = id
        self.name = name
        self.lifePoints = lifePoints

    def __repr__(self):
        return f"<Bestiary id={self.id} name={self.name!r} lifePoints={self.lifePoints}>"

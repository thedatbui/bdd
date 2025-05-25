class Bestiary:
    def __init__(self, id, name, attributes, attack, defense, lifePoints):
        self.id = id
        self.name = name
        self.attributes = attributes
        self.attack = attack
        self.defense = defense
        self.lifePoints = lifePoints

    def __str__(self):
        return f"Bestiary: {self.name}, Attributes: {self.attributes}, Attack: {self.attack}, Defense: {self.defense}, Life Points: {self.lifePoints}"
    
    def getId(self):
        return self.id
    
    def getName(self):
        return self.name
    
    def getAttributes(self):
        return self.attributes
    
    def getAttack(self):
        return self.attack
    
    def getDefense(self):
        return self.defense
    
    def getLifePoints(self):
        return self.lifePoints
    
    def setId(self, id):
        self.id = id

    def setName(self, name):
        self.name = name

    def setAttributes(self, attributes):
        self.attributes = attributes

    def setAttack(self, attack):
        self.attack = attack

    def setDefense(self, defense):
        self.defense = defense

    def setLifePoints(self, lifePoints):
        self.lifePoints = lifePoints

class Object:
    def __init__(self, name, type_, strength, defence, effects, price):
        self.name = name
        self.type_ = type_
        self.strength = strength
        self.defence = defence
        self.effects = effects
        self.price = price

    def getName(self):
        return self.name
    
    def getType(self):
        return self.type_
    
    def getStrength(self):
        return self.strength
    
    def getDefence(self):
        return self.defence
    
    def getEffects(self):
        return self.effects
    
    def getPrice(self):
        return self.price
    
    def setAttribute(self, name, type_, strength, defence, effects, price):
        self.name = name
        self.type_ = type_
        self.strength = strength
        self.defence = defence
        self.effects = effects
        self.price = price
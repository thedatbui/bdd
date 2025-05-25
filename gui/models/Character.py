class Character:
    def __init__(self, Id, name, classe, strength, intelligence, agility, pv, mana):
        self.Id = Id
        self.name = name
        self.classe = classe
        self.strength = strength
        self.intelligence = intelligence
        self.agility = agility
        self.pv = pv
        self.mana = mana
    
    def __str__(self):
        return f"Character({self.Id} {self.name}, {self.classe}, {self.strength}, {self.intelligence}, {self.agility}, {self.pv}, {self.mana})"
    
    def setAttribute(self, attribute, value):
        if attribute == "Id":
            self.Id = value
        elif attribute == "name":
            self.name = value
        elif attribute == "classe":
            self.classe = value
        elif attribute == "strength":
            self.strength = value
        elif attribute == "intelligence":
            self.intelligence = value
        elif attribute == "agility":
            self.agility = value
        elif attribute == "pv":
            self.pv = value
        elif attribute == "mana":
            self.mana = value
        else:
            raise ValueError(f"Unknown attribute: {attribute}")
        
    def getAttribute(self, attribute):
        if attribute == "Id":
            return self.Id
        if attribute == "name":
            return self.name
        elif attribute == "classe":
            return self.classe
        elif attribute == "strength":
            return self.strength
        elif attribute == "intelligence":
            return self.intelligence
        elif attribute == "agility":
            return self.agility
        elif attribute == "pv":
            return self.pv
        elif attribute == "mana":
            return self.mana
        else:
            raise ValueError(f"Unknown attribute: {attribute}")
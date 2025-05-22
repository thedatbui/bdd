class Npc :
    def __init__(self, Id, name, dialogue, type_):
        self.Id = Id
        self.name = name
        self.dialogue = dialogue
        self.type = type_

    def __str__(self):
        return f"{self.name}: {self.dialogue} (Location: {self.type})"
    
    def getId(self):
        return self.Id
    
    def getName(self):
        return self.name
    
    def getDialogue(self):
        return self.dialogue
    
    def getType(self):
        return self.type

    def setId(self, Id):
        self.Id = Id
    
    def setName(self, name):
        self.name = name

    def setDialogue(self, dialogue):
        self.dialogue = dialogue

    def setType(self, type_):
        self.type = type_
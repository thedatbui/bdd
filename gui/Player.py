from gui.Character import Character
from src.db_utils.connectToDataBase import *

class Player():
    def __init__(self, name, Id):
        self.name = name
        self.Id = Id

        self.characterSeleted = None
        self.character = Character(None, None, None, None, None, None, None)
        self.characterList = []

        self.cursor = get_cursor()

    def getName(self):
        return self.name
    
    def getId(self):
        return self.Id
    
    def setName(self, name):
        self.name = name

    def setId(self, Id):
        self.Id = Id

    def setCharacterSelected(self, character):
        self.characterSeleted = character

    def getCharacterSelected(self):
        return self.characterSeleted
    
    def addCharacter(self, character):
        if len(self.characterList) == 0:
            self.characterList.append(character)
        else:
            for char in self.characterList:
                if char.getAttribute("name") != character.getAttribute("name"):
                    self.characterList.append(character)
                
    
    def removeCharacter(self, character):
        if character in self.characterList:
            self.characterList.remove(character)
        else:
            raise ValueError("Character not found in the list.")
    
    def getCharacterList(self):
        return self.characterList

    def setCharacter(self, character):
        self.character = character

    def getCharacter(self):
        return self.character
    
    def __str__(self):
        return f"Player Name: {self.name}, Player ID: {self.Id}"
    
    def getCharacterFromDatabase(self):
        query = "SELECT * FROM `Character` WHERE PlayerID = %s"
        self.cursor.execute(query, (self.Id,))
        
        # Get column names from cursor.description
        columns = [desc[0] for desc in self.cursor.description]
        
        # Fetch all rows (use fetchall instead of fetchone to get multiple rows)
        results = self.cursor.fetchall()

        if results:
            for row in results:
                character_data = dict(zip(columns, row))
                character = Character(
                    name=character_data['CharacterName'],
                    classe=character_data['Class'],
                    strength=character_data['Strength'],
                    intelligence=character_data['Intelligence'],
                    agility=character_data['Agility'],
                    pv=character_data['pv'],
                    mana=character_data['mana']
                )
                self.addCharacter(character)
    
        
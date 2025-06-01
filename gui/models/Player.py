from gui.models.Character import Character
from src.db_utils.connectToDataBase import *
from gui.service.inventory_service import InventoryService
from gui.service.character_service import CharacterService


class Player():
    def __init__(self, name, Id, Xp, money, level, inventorySlot):
        self.name = name
        self.Id = Id
        self.money = money
        self.Xp = Xp
        self.level = level
        self.inventorySlot = inventorySlot
        self.characterSeleted = None
        self.npc = None
        self.character = Character(None, None, None, None, None, None, None, None)
        self.characterList = []
        self.inventory = InventoryService()
        self.characterService = CharacterService()
 

    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
        
    def getId(self):
        return self.Id
    
    def getMoney(self):
        return self.money
    
    def getLevel(self):
        return self.level

    def getCharacter(self):
        return self.character

    def getInventorySlot(self):
        return self.inventorySlot
    
    def getCharacterList(self):
        return self.characterList
    
    def getCharacterSelected(self):
        return self.characterSeleted
    
    def getXp(self):
        return self.Xp
    
    def getNpc(self):
        return self.npc
    
    def setNpc(self, npc):
        self.npc = npc
    
    def setXp(self, xp):
        if xp >= 0:
            self.Xp = xp
        else:
            raise ValueError("XP cannot be negative.")
        
    def setMoney(self, money):
        if money >= 0:
            self.money = money
        else:
            raise ValueError("Money cannot be negative.")
        
    def setLevel(self, level):
        if level >= 0:
            self.level = level
        else:
            raise ValueError("Level cannot be negative.")
        
    def setInventorySlot(self, inventorySlot):
        if inventorySlot >= 0:
            self.inventorySlot = inventorySlot
        else:
            raise ValueError("Inventory slot cannot be negative.")
        
    def setAttribute(self, name, Id, money, level, inventorySlot):
        self.name = name
        self.Id = Id
        self.money = money
        self.level = level
        self.inventorySlot = inventorySlot

    def setCharacterSelected(self, character):
        self.characterSeleted = character

    def isInCharacterList(self, character):
        for char in self.characterList:
            if char.getAttribute("name") == character.getAttribute("name"):
                return True
        return False
    
    def addCharacter(self, character):
        if len(self.characterList) == 0:
            self.characterList.append(character)
        else:
            if not self.isInCharacterList(character):
                self.characterList.append(character)
                    
                
    def removeCharacter(self, character):
        if character in self.characterList:
            self.characterList.remove(character)
        else:
            raise ValueError("Character not found in the list.")
    
    def setCharacter(self, character):
        self.character = character

    def __str__(self):
        return f"Player Name: {self.name}, Player ID: {self.Id}"
    
    def getCharacterFromDatabase(self):
        characterList = self.characterService.get_characters_by_player_id(self.Id)
        return characterList
        
    def addItemToInventory(self, itemName):
        self.inventory.update_attribute(self.Id, "MaxCapacity", self.inventorySlot)
        self.inventory.add_item(self.Id, self.characterSeleted.getAttribute("Id"), itemName, self.inventorySlot)
        print("Item added to inventory.")
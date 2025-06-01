from gui.models.Character import Character
from gui.service.db_service import DatabaseService

class CharacterService:
    """Service for character operations."""
    
    def __init__(self):
        """Initialize the character service."""
        self.db_service = DatabaseService()
    
    def get_characters_by_player_id(self, player_id):
        """
        Get all characters for a player.
        
        Args:
            player_id (int): The player's ID
            
        Returns:
            list: List of Character objects
        """
        query = "SELECT * FROM CharacterTable WHERE PlayerID = %s"
        if not self.db_service.execute_query(query, (player_id,)):
            return []
        
        results = self.db_service.fetch_all()
        characters = []
        
        for result in results:
            # Assuming: ID, PlayerID, CharacterName, Class, Strength, Agility, Intelligence, pv, mana
            character = Character(
                Id=result[0],
                name=result[2],
                classe=result[3],
                strength=result[4],
                intelligence=result[6],
                agility=result[5],
                pv=result[7],
                mana=result[8]
            )
            characters.append(character)
        
        return characters
    
    def check_character_exists(self, character_name):
        """
        Check if a character exists.
        
        Args:
            character_name (str): The character's name
            
        Returns:
            bool: True if exists, False otherwise
        """
        query = "SELECT * FROM CharacterTable WHERE CharacterName = %s"
        self.db_service.execute_query(query, (character_name,))
        return self.db_service.fetch_one() is not None and self.db_service.commit()
    
    def create_character(self, player_id, character):
        """
        Create a new character.
        
        Args:
            player_id (int): The player's ID
            character (Character): The character to create
            
        Returns:
            (bool, str): Tuple of (success, message)
        """
        # Check if character already exists
        if self.check_character_exists(character.name):
            return False, f"Character {character.name} already exists."
        
        # Create the character
        query = """
        INSERT INTO CharacterTable
        (PlayerID, CharacterName, Class, Strength, Agility, Intelligence, pv, mana) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            player_id,
            character.name,
            character.classe,
            character.strength,
            character.agility,
            character.intelligence,
            character.pv,
            character.mana,
        )
        
        if not self.db_service.execute_query(query, values):
            return False, "Failed to create character."
        
        if not self.db_service.commit():
            return False, "Failed to save character to database."
        
        return True, f"Character {character.name} created successfully."
    
    def delete_character(self, characterId, player_id):
        """
        Delete a character.
        
        Args:
            character_name (str): The character's name
            player_id (int): The player's ID
            
        Returns:
            (bool, str): Tuple of (success, message)
        """
        query = "DELETE FROM CharacterTable WHERE ID = %s AND PlayerID = %s"
        if not self.db_service.execute_query(query, (characterId, player_id)):
            return False, f"Failed to delete character: {characterId}"
        
        self.db_service.commit()
        return True, f"Character {characterId} deleted successfully."
    
    def insert_character_killQuest(self, characterId, quest, beast, count):
        """
        Insert a new character quest.
        
        Args:
            characterId (int): The character's ID
            quest (str): The quest name
            beast (str): The beast name
            count (int): The kill count
            
        Returns:
            bool: True if successful, False otherwise
        """
        # first check if the quest already exists for the character
        query = "SELECT * FROM CharacterQuest WHERE CharacterID = %s AND QuestName = %s"
        self.db_service.execute_query(query, (characterId, quest))
        if self.db_service.fetch_one() is not None:
            return False
        
        query = """
        INSERT INTO CharacterQuest (CharacterID, QuestName, BeastName, killNumber) 
        VALUES (%s, %s, %s, %s)
        """
        values = (characterId, quest, beast, count)
        
        if not self.db_service.execute_query(query, values):
            return False
        
        return self.db_service.commit()
    
    def select_quest(self, characterId, quest):
        """
        Select a quest for a character.
        
        Args:
            characterId (int): The character's ID
            quest (str): The quest to select
            
        Returns:
            bool: True if successful, False otherwise
        """
        query = "UPDATE CharacterTable SET Quest_In_Progress = %s WHERE ID = %s"
        if not self.db_service.execute_query(query, (quest, characterId)):
            return False
        
        if not self.db_service.commit():
            return False
        
        return True
    
    def update_beast_killed(self, characterId, questName, beastKilled):
        """
        Update the number of beasts killed by a character.
        
        Args:
            characterId (int): The character's ID
            beastKilled (int): The number of beasts killed
            
        Returns:
            bool: True if successful, False otherwise
        """
        query = "UPDATE CharacterQuest SET BeastKilled = %s WHERE CharacterID = %s AND QuestName = %s"
        if not self.db_service.execute_query(query, (beastKilled, characterId, questName)):
            return False
        
        if not self.db_service.commit():
            return False
        return True
    
    def get_beast_killed(self, characterID, quest):
        """
        Get the number of beasts killed by a character.
        
        Returns:
            int: The number of beasts killed or None if not found
        """
        query = "SELECT BeastKilled FROM CharacterQuest WHERE CharacterID = %s AND QuestName = %s"
        if not self.db_service.execute_query(query, (characterID, quest)):
            return False
        result = self.db_service.fetch_one()
        print(f"get_beast_killed query: {query} with params: {characterID}, {quest}")
        print(f"get_beast_killed: {result}")
        if not self.db_service.commit():
            return False
        return result[0] if result else None
    
    def get_count(self, quest):
        """
        Get the count objective for a quest.
        
        Args:
            quest (str): The quest name
            
        Returns:
            int: The count objective or None if not found
        """
        query = "SELECT killNumber FROM CharacterQuest WHERE QuestName = %s"
        if not self.db_service.execute_query(query, (quest,)):
            return False
        result = self.db_service.fetch_one()
        self.db_service.commit()
        return result[0] if result else None
        
    def get_selected_quest(self, characterId):
        """
        Get the selected quest for a character.
        
        Args:
            characterId (int): The character's ID
            
        Returns:
            str: The selected quest name or None if not found
        """
        query = "SELECT Quest_In_Progress FROM CharacterTable WHERE ID = %s"
        if not self.db_service.execute_query(query, (characterId,)):
            return False
        result = self.db_service.fetch_one()
        self.db_service.commit()
        return result[0] if result else None
    
    def get_beast_to_kill(self, characterId, quest):
        """
        Get the beast to kill for a character's quest.
        
        Args:
            characterId (int): The character's ID
            
        Returns:
            str: The beast name or None if not found
        """
        query = "SELECT BeastName FROM CharacterQuest WHERE CharacterID = %s AND QuestName = %s"
        if not self.db_service.execute_query(query, (characterId, quest)):
            return False
        result = self.db_service.fetch_one()
        self.db_service.commit()
        return result[0] if result else None
    
    def get_quest_list(self, characterId):
        """
        Get the list of quests for a character.
        
        Args:
            characterId (int): The character's ID
            
        Returns:
            list: List of quest names
        """
        query = "SELECT QuestName FROM CharacterQuest WHERE CharacterID = %s"
        self.db_service.execute_query(query, (characterId,))
        results = self.db_service.fetch_all()
        self.db_service.commit()
        return [result[0] for result in results] if results else []
    
    def remove_quest(self, characterId, quest):
        """
        Remove a quest from a character.
        
        Args:
            characterId (int): The character's ID
            quest (str): The quest name
            
        Returns:
            bool: True if successful, False otherwise
        """
        query = "DELETE FROM CharacterQuest WHERE CharacterID = %s AND QuestName = %s"
        if not self.db_service.execute_query(query, (characterId, quest)):
            return False
        
        return self.db_service.commit()
    
    def select_next_quest(self, characterId):
        """
        Select the next quest for a character.
        Sets Quest_In_Progress to NULL if no quests are available.
        
        Args:
            characterId (int): The character's ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        # First check if there are any quests available
        query = "SELECT QuestName FROM CharacterQuest WHERE CharacterID = %s AND BeastKilled < killNumber ORDER BY QuestName LIMIT 1"
        self.db_service.execute_query(query, (characterId,))
        result = self.db_service.fetch_one()
        
        # Prepare to update the character's Quest_In_Progress
        next_query = "UPDATE CharacterTable SET Quest_In_Progress = %s WHERE ID = %s"
        
        if result:
            # If a quest is available, set it as the current quest
            quest_name = result[0]
            if not self.db_service.execute_query(next_query, (quest_name, characterId)):
                return False
        else:
            # If no quests are available, set Quest_In_Progress to NULL
            if not self.db_service.execute_query(next_query, (None, characterId)):
                return False
        
        # Commit the changes
        return self.db_service.commit()
    
    def calculate_xp_for_next_level(self, current_level):
        """
        Calculate the XP required for the next level.
        Formula: 100 * (current_level ^ 1.5)
        """
        return int(100 * (current_level ** 1.5))

    def add_experience(self, character_id, xp_gained):
        """
        Add experience points to a character and handle level up if necessary.
        
        Args:
            character_id (int): The character's ID
            xp_gained (int): The amount of XP to add
            
        Returns:
            dict: Information about the level up if it occurred
        """
        # Get current XP and level
        self.db_service.execute_query(
            "SELECT ExperiencePoints, PlayerLevel FROM Player p JOIN CharacterTable c ON p.ID = c.PlayerID WHERE c.ID = %s",
            (character_id,)
        )
        result = self.db_service.fetch_one()
        if not result:
            return None
        
        current_xp, current_level = result
        new_xp = current_xp + xp_gained
        xp_for_next = self.calculate_xp_for_next_level(current_level)
        
        level_up_info = None
        levels_gained = 0
        
        # Check for level up
        while new_xp >= xp_for_next:
            current_level += 1
            levels_gained += 1
            new_xp -= xp_for_next
            xp_for_next = self.calculate_xp_for_next_level(current_level)
            
            # Update inventory slots (base 10 + 2 per level after 1)
            new_slots = 10 + (2 * (current_level - 1))
            self.db_service.execute_query(
                "UPDATE Player SET InventorySlot = %s WHERE ID = (SELECT PlayerID FROM CharacterTable WHERE ID = %s)",
                (new_slots, character_id)
            )
            
            level_up_info = {
                'old_level': current_level - levels_gained,
                'new_level': current_level,
                'remaining_xp': new_xp,
                'next_level_xp': xp_for_next
            }
        
        # Add attribute points for all levels gained at once
        if levels_gained > 0:
            self.add_attribute_points(character_id, 2 * levels_gained)
        
        # Update XP and level
        self.db_service.execute_query(
            "UPDATE Player SET ExperiencePoints = %s, PlayerLevel = %s WHERE ID = (SELECT PlayerID FROM CharacterTable WHERE ID = %s)",
            (new_xp, current_level, character_id)
        )
        self.db_service.commit()
        return level_up_info

    def get_attribute_points(self, character_id):
        """
        Get the number of attribute points available for a character.
        
        Args:
            character_id (int): The character's ID
            
        Returns:
            int: Number of attribute points available
        """
        query = "SELECT AttributePoints FROM CharacterTable WHERE ID = %s"
        self.db_service.execute_query(query, (character_id,))
        result = self.db_service.fetch_one()
        self.db_service.commit()
        return result[0] if result else 0

    def add_attribute_points(self, character_id, points):
        """
        Add attribute points to a character.
        
        Args:
            character_id (int): The character's ID
            points (int): Number of points to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        query = "UPDATE CharacterTable SET AttributePoints = AttributePoints + %s WHERE ID = %s"
        if not self.db_service.execute_query(query, (points, character_id)):
            return False
        return self.db_service.commit()

    def use_attribute_point(self, character_id, attribute):
        """
        Use an attribute point to increase a character's attribute.
        
        Args:
            character_id (int): The character's ID
            attribute (str): The attribute to increase ('Strength', 'Agility', or 'Intelligence')
            
        Returns:
            bool: True if successful, False otherwise
        """
        # First check if we have points available
        if self.get_attribute_points(character_id) <= 0:
            return False
            
        # Update the attribute and decrease points
        query = f"""
        UPDATE CharacterTable 
        SET {attribute} = {attribute} + 1,
            AttributePoints = AttributePoints - 1
        WHERE ID = %s
        """
        if not self.db_service.execute_query(query, (character_id,)):
            return False
        return self.db_service.commit()
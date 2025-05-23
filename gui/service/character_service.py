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
        return self.db_service.fetch_one() is not None
    
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
            character.mana
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
        # delete related items
        query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_NAME = 'CharacterTable';"
        self.db_service.execute_query(query)
        results = self.db_service.fetch_all()
        for result in results:
            table_name = result[0]
            print(table_name)
            query = f"DELETE FROM {table_name} WHERE CharacterID = %s"
            if not self.db_service.execute_query(query, (characterId,)):
                return False, f"Failed to delete related data from {table_name}."
            
        query = "DELETE FROM CharacterTable WHERE ID = %s AND PlayerID = %s"
        if not self.db_service.execute_query(query, (characterId, player_id)):
            return False, f"Failed to delete character: {characterId}"
        
        if not self.db_service.commit():
            return False, "Failed to commit character deletion."
        
        return True, f"Character {characterId} deleted successfully."
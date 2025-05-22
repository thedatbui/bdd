from gui.models.Player import Player
from gui.service.db_service import DatabaseService

class PlayerService:
    """Service for player operations."""
    
    def __init__(self):
        """Initialize the player service."""
        self.db_service = DatabaseService()
    
    def get_player_by_username(self, username):
        """
        Get a player by username.
        
        Args:
            username (str): The username to lookup
            
        Returns:
            Player or None if not found
        """
        query = "SELECT * FROM Player WHERE UserName = %s"
        self.db_service.execute_query(query, (username,))
        result = self.db_service.fetch_one()
        
        if result:
            # Assuming: ID, UserName
            player = Player(name=result[1], Id=result[0], money=result[3], level=result[2], inventorySlot=result[5])
            return player
        return None
    
    def create_player(self, username):
        """
        Create a new player.
        
        Args:
            username (str): The new player's username
            
        Returns:
            (Player, str): Tuple of (Player object, success/error message)
        """
        # Check if player already exists
        query = "SELECT * FROM Player WHERE UserName = %s"
        self.db_service.execute_query(query, (username,))
        result = self.db_service.fetch_one()
        
        if result:
            return None, f"Username {username} already exists."
        
        # Create new player
        query = "INSERT INTO Player (UserName) VALUES (%s)"
        if not self.db_service.execute_query(query, (username,)):
            return None, "Failed to create player account."
        
        if not self.db_service.commit():
            return None, "Failed to save player account to database."
        
        # Get the new player
        return self.get_player_by_username(username), f"Account {username} created successfully."
    
    def delete_player(self, player):
        """
        Delete a player.
        
        Args:
            player (Player): The player to delete
            
        Returns:
            (bool, str): Tuple of (success, message)
        """
        # delete related data first
        query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_NAME = 'Player';"
        self.db_service.execute_query(query)
        results = self.db_service.fetch_all()
        for result in results:
            table_name = result[0]
            query = f"DELETE FROM {table_name} WHERE PlayerID = %s"
            if not self.db_service.execute_query(query, (player.getId(),)):
                return False, f"Failed to delete related data from {table_name}."
        
        query = "DELETE FROM Player WHERE UserName = %s"
        if not self.db_service.execute_query(query, (player.getName(),)):
            return False, f"Failed to delete account: {player.getName()}"
        
        if not self.db_service.commit():
            return False, "Failed to commit account deletion."
        
        return True, f"Account {player.getName()} deleted successfully."
    
    def update_player_username(self, player, new_username):
        """
        Update a player's username.
        Args:
            player (Player): The player to update
            new_username (str): The new username
        Returns:
            (bool, str): Tuple of (success, message)
        """
        # Check if new username already exists
        query = "SELECT * FROM Player WHERE UserName = %s"
        self.db_service.execute_query(query, (new_username,))
        result = self.db_service.fetch_one()
        
        if result:
            return False, f"Username {new_username} already exists."
        
        # Get the current username from the player object
        current_username = player.getName()
        
        # Update username in database
        query = "UPDATE Player SET UserName = %s WHERE UserName = %s"
        if not self.db_service.execute_query(query, (new_username, current_username)):
            return False, f"Failed to update username in database."
        
        if not self.db_service.commit():
            return False, "Failed to commit username change."
        
        # Update the username in the player object
        player.setName(new_username)
        return True, f"Username updated successfully to {new_username}."
            
        
       
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
    
    def insert_player(self, player):
        """
        Insert a new player into the database.
        
        Args:
            player (Player): The player to insert
            
        Returns:
            (bool, str): Tuple of (success, message)
        """
        query = "INSERT INTO Player (UserName) VALUES (%s)"
        if not self.db_service.execute_query(query, (player.getName(),)):
            return False, "Failed to insert player into database."
        
        if not self.db_service.commit():
            return False, "Failed to commit player insertion."
        
        return True, f"Player {player.getName()} inserted successfully."
    
    def recursive_delete_player(self, key_value, table_name, key_column='ID'):
        """
        Supprime récursivement les données liées à un joueur en suivant les clés étrangères.

        Args:
            key_value (any): La valeur de la clé (par ex. Player.ID)
            table_name (str): Le nom de la table principale (ex: "Player")
            key_column (str): Le nom de la colonne clé (ex: "ID" pour Player)

        Returns:
            (bool, str): Tuple de réussite
        """
        # Trouve les tables qui référencent cette table
        query = """
            SELECT TABLE_NAME, COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE REFERENCED_TABLE_NAME = %s
            AND REFERENCED_COLUMN_NAME = %s
            AND TABLE_SCHEMA = DATABASE()
        """
        self.db_service.execute_query(query, (table_name, key_column))
        results = self.db_service.fetch_all()

        for child_table, foreign_key_column in results:
            # Suppression récursive des données dans les tables enfants
            success, message = self.recursive_delete_player(key_value, child_table, foreign_key_column)
            if not success:
                return False, message

            # Supprimer les lignes associées
            delete_query = f"DELETE FROM {child_table} WHERE {foreign_key_column} = %s"
            if not self.db_service.execute_query(delete_query, (key_value,)):
                return False, f"Échec de suppression dans {child_table} (clé: {foreign_key_column})"

        return True, "Suppression récursive réussie."

            
    def delete_player(self, player):
        """
        Supprime un joueur et toutes les données liées.

        Args:
            player (Player): Objet joueur à supprimer

        Returns:
            (bool, str): Succès, message
        """
        player_id = player.getID()  # Il te faut une méthode getID() dans Player

        # Supprimer les données liées
        success, message = self.recursive_delete_player(player_id, "Player", "ID")
        if not success:
            return False, message

        # Supprimer le joueur lui-même
        delete_query = "DELETE FROM Player WHERE ID = %s"
        if not self.db_service.execute_query(delete_query, (player_id,)):
            return False, "Échec de suppression du joueur"

        if not self.db_service.commit():
            return False, "Échec du commit"

        return True, f"Le joueur ID {player_id} a été supprimé avec succès."

    
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
    
    def check_existing_username(self, username):
        """
        Check if a username already exists.
        
        Args:
            username (str): The username to check
            
        Returns:
            bool: True if exists, False otherwise
        """
        query = "SELECT * FROM Player WHERE UserName = %s"
        self.db_service.execute_query(query, (username,))
        result = self.db_service.fetch_one()
        
        return result is not None
    
            
        
       
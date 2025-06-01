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
            player = Player(name=result[1], Id=result[0], Xp=result[3], money=result[4], level=result[2], inventorySlot=result[5])
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

    def delete_player(self, player):
        """
        Supprime un joueur et toutes les données liées.

        Args:
            player (Player): Objet joueur à supprimer

        Returns:
            (bool, str): Succès, message
        """
        player_id = player.getId()
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
    
    def update_player_wallet(self, player_id, amount):
        """
        Update the player's wallet.
        
        Args:
            player_id (int): The player's ID
            amount (int): The amount to add/subtract
            
        Returns:
            bool: True if successful, False otherwise
        """
        query = "UPDATE Player SET WalletCredits = %s  WHERE ID = %s"
        if not self.db_service.execute_query(query, (amount, player_id)):
            return False
        
        return self.db_service.commit()
    
    def get_wallet_for_character(self, character_id):
        """
        Récupère le solde d'or (WalletCredits) du personnage.
        """
        self.db_service.execute_query(
            "SELECT WalletCredits FROM Player p JOIN CharacterTable c ON p.ID = c.PlayerID WHERE c.ID = %s",
            (character_id,)
        )
        row = self.db_service.fetch_one()
        return (row or (0,))[0]

    def update_wallet(self, character_id, amount):
        """
        Met à jour le solde d'or du personnage de manière sécurisée.
        
        Args:
            character_id (int): L'ID du personnage
            amount (int): Le montant à ajouter (positif) ou retirer (négatif)
            
        Returns:
            bool: True si la transaction a réussi, False sinon
        """
        # Vérifier que le montant est valide
        if amount == 0:
            return True
            
        # Récupérer le solde actuel
        current_balance = self.get_wallet_for_character(character_id)
        new_balance = current_balance + amount
        
        # Vérifier que le nouveau solde ne sera pas négatif
        if new_balance < 0:
            return False
            
        # Mettre à jour le solde
        self.db_service.execute_query(
            "UPDATE Player p JOIN CharacterTable c ON p.ID = c.PlayerID SET p.WalletCredits = %s WHERE c.ID = %s",
            (new_balance, character_id)
        )
        
        return self.db_service.commit()
        
       
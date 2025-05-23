from gui.service.db_service import DatabaseService
from gui.models.Object import Object

class InventoryService:
    """Service for inventory operations."""
    
    def __init__(self):
        """Initialize the inventory service."""
        self.db_service = DatabaseService()
    
    def get_inventory_items(self, characterId):
        """
        Get all items in the inventory for a player.
        
        Args:
            player_id (int): The player's ID
            
        Returns:
            list: List of Object objects
        """
        query = "SELECT * FROM Inventory WHERE characterID = %s"
        if not self.db_service.execute_query(query, (characterId,)):
            return []
        
        results = self.db_service.fetch_all()
        items = []
        
        for result in results:
            print(result)
            items.append(result[2])
        return items
    
    def update_attribute(self, player_id, attribute, value):
        """
        Update a specific attribute of a player.
        
        Args:
            player_id (int): The player's ID
            attribute (str): The attribute to update
            value (int): The new value
            
        Returns:
            bool: True if successful, False otherwise
        """
        query = f"UPDATE Inventory SET {attribute} = %s WHERE PlayerID = %s"
        return self.db_service.execute_query(query, (value, player_id))
    
    def get_item_details(self, item_name):
        """
        Get details of a specific item.
        
        Args:
            item_name (str): The item's name
            
        Returns:
            Object: The Object object with details
        """
        query = "SELECT * FROM ObjectTest WHERE ObjectName = %s"
        if not self.db_service.execute_query(query, (item_name,)):
            return None
        
        result = self.db_service.fetch_one()
        if result:
            return Object(result[1], result[2], result[3], result[4], result[5], result[6])
        
        return None

    def add_item(self, player_id, characterId, item_name, item_slot):
        """
        Add an item to the inventory.
        
        Args:
            player_id (int): The player's ID
            item_name (str): The item's name
            
        Returns:
            bool: True if successful, False otherwise
        """
        query = "INSERT INTO Inventory (PlayerID, CharacterID, ObjectName, MaxCapacity) VALUES (%s, %s, %s, %s)"
        return self.db_service.execute_query(query, (player_id, characterId , item_name, item_slot))
    
    def delete_item(self, player_id, item_name):
        """
        Delete an item from the inventory.
        
        Args:
            item_name (str): The item's name
            
        Returns:
            bool: True if successful, False otherwise
        """
        query = "DELETE FROM Inventory WHERE PlayerID = %s AND ObjectName = %s"
        return self.db_service.execute_query(query, (player_id, item_name))
    
    def check_existing_item(self, player_id, item_name):
        """
        Check if an item already exists in the inventory.
        
        Args:
            player_id (int): The player's ID
            item_name (str): The item's name
            
        Returns:
            bool: True if exists, False otherwise
        """
        query = "SELECT * FROM Inventory WHERE PlayerID = %s AND ObjectName = %s"
        if not self.db_service.execute_query(query, (player_id, item_name)):
            return False
        
        result = self.db_service.fetch_one()
        if result:
            return True, result[3]
        return False, None
    
    def get_item_quantity(self, character_id, item_name):
        """
        Get the quantity of an item in the inventory.
        
        Args:
            player_id (int): The player's ID
            item_name (str): The item's name
            
        Returns:
            int: The quantity of the item
        """
        query = "SELECT Quantity FROM Inventory WHERE CharacterID = %s AND ObjectName = %s"
        if not self.db_service.execute_query(query, (character_id, item_name)):
            return 0
        
        result = self.db_service.fetch_one()
        if result:
            return result[0]
        
        return 0

    def update_quantity(self, characterID, item_name, quantity):
        """
        Update the quantity of an item in the inventory.
        
        Args:
            player_id (int): The player's ID
            item_name (str): The item's name
            quantity (int): The new quantity
            
        Returns:
            bool: True if successful, False otherwise
        """
        query = "UPDATE Inventory SET Quantity = %s WHERE CharacterID = %s AND ObjectName = %s"
        return self.db_service.execute_query(query, (quantity, characterID, item_name))
    
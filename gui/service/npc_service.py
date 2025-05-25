from gui.models.Player import *
from gui.models.Npc import *
from gui.models.Quest import Quest
from gui.service.db_service import DatabaseService


class NpcService:
    """Service for NPC operations."""
    
    def __init__(self):
        """Initialize the NPC service."""
        self.db_service = DatabaseService()
    
    def get_npc(self):
        """
        Get an NPC by ID.
        
        Args:
            npc_id (int): The ID of the NPC to lookup
            
        Returns:
            Npc or None if not found
        """
        query = "SELECT * FROM NPC"
        self.db_service.execute_query(query)
        result = self.db_service.fetch_all()
        npc_list = []
        if result:
            for row in result:
                npc = Npc(row[0], row[1], row[2], row[3])
                npc_list.append(npc)
        return npc_list
    
    def get_quest_npc(self, npc_id):
        """
        Get NPCs associated with a specific quest.
        
        Args:
            quest_id (int): The ID of the quest
            
        Returns:
            List of Npc objects or empty list if none found
        """
        quest_list = []
        query = "SELECT QuestName FROM NPCQuest WHERE NPCID = %s"
        if not self.db_service.execute_query(query, (npc_id,)):
            return []
        result = self.db_service.fetch_all()
        if result:
            for row in result:
                quest_list.append(row[0])
        return quest_list
    
    def check_existing_quest(self, quest_name):
        """
        Check if a quest exists.
        
        Args:
            quest_name (str): The name of the quest
            
        Returns:
            bool: True if the quest exists, False otherwise
        """
        query = "SELECT * FROM Quest WHERE QuestName = %s"
        if not self.db_service.execute_query(query, (quest_name,)):
            return False
        
        result = self.db_service.fetch_one()
        return result is not None
    
    def get_quest_details(self, quest_name):
        """
        Get details of a specific quest.
        
        Args:
            quest_name (str): The name of the quest
            
        Returns:
            List of Npc objects associated with the quest
        """
        query = "SELECT * FROM Quest WHERE QuestName = %s"
        if not self.db_service.execute_query(query, (quest_name,)):
            print(f"Quest '{quest_name}' not found.")
            return None
        
        result = self.db_service.fetch_one()
        if result:
            return Quest(result[0], result[1], result[2], result[3], result[4])
        return None
    
    def get_item_details(self, item_id):
        """
        Get details of a specific item.
        
        Args:
            item_name (str): The name of the item
            
        Returns:
            List of Npc objects associated with the item
        """
        query = "SELECT ObjectTest.ObjectName, ObjectTest.price, NPCInventory.Quantity FROM ObjectTest, NPCInventory " \
        "WHERE NPCInventory.ObjectName = ObjectTest.ObjectName AND NPCInventory.NPCID = %s;"
        if not self.db_service.execute_query(query, (item_id,)):
            return None
        item_list = []
        result = self.db_service.fetch_all()
        if result:
            for row in result:
                item = f"{row[0]} - {row[1]} gold - {row[2]} available"
                item_list.append(item)
        return item_list
            
       

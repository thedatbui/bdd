from gui.models.Player import *
from gui.models.Npc import *
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

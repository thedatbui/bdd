from gui.models.Bestiary import Bestiary
from gui.service.db_service import DatabaseService

class BestiaryService:
    """Service for managing the bestiary."""

    def __init__(self):
        """Initialize the bestiary service."""
        self.db_service = DatabaseService()

    def get_bestiaryName(self):
        """Retrieve a bestiary entry by its ID."""
        bestiaryList = []
        query = "SELECT * FROM Bestiary"
        if not self.db_service.execute_query(query):
            return []
        
        result = self.db_service.fetch_all()
        for row in result:
            bestiaryList.append(row[1])
        return bestiaryList
    
    def get_bestiary_details(self, name):
        """Retrieve details of a specific bestiary entry by its name."""
        query = "SELECT * FROM Bestiary WHERE BeastName = %s"
        print(name)
        if not self.db_service.execute_query(query, (name,)):
            return None
        
        result = self.db_service.fetch_one()
        print(result)
        if result:
            return Bestiary(result[0], result[1], result[2], result[3], result[4], result[5])
        return None

       
     
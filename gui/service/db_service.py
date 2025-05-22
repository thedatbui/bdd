from src.db_utils.connectToDataBase import get_connection, get_cursor

class DatabaseService:
    """Service for database operations."""
    
    def __init__(self):
        """Initialize the database service."""
        self.connection = get_connection()
        self.cursor = get_cursor()
    
    def execute_query(self, query, params=None):
        """
        Execute a database query.
        
        Args:
            query (str): SQL query to execute
            params (tuple, optional): Parameters for the query
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return True
        except Exception as e:
            print(f"Database error: {e}")
            return False
    
    def fetch_one(self):
        """
        Fetch one result from the executed query.
        
        Returns:
            The result or None if no result
        """
        return self.cursor.fetchone()
    
    def fetch_all(self):
        """
        Fetch all results from the executed query.
        
        Returns:
            List of results or empty list if no results
        """
        return self.cursor.fetchall()
    
    def commit(self):
        """Commit the transaction."""
        try:
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Commit error: {e}")
            return False
    
    def close(self):
        """Close the database connection."""
        try:
            self.cursor.close()
            self.connection.close()
            return True
        except Exception as e:
            print(f"Close error: {e}")
            return False
from src.db_utils.connectToDataBase import get_connection, get_cursor
import mysql.connector

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
            # Clear any unread results before executing a new query
            self.clear_cursor()
            
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
        try:
            return self.cursor.fetchone()
        except mysql.connector.errors.InterfaceError as e:
            pass
    
    def fetch_all(self):
        """
        Fetch all results from the executed query.
        
        Returns:
            List of results or empty list if no results
        """
        try:
            return self.cursor.fetchall()
        except mysql.connector.errors.InterfaceError as e:
            pass
    
    def safe_fetch_all(self):
        """
        Safely fetch all remaining results, without raising an exception if there are none.
        
        Returns:
            List of results or empty list if no results available
        """
        try:
            return self.cursor.fetchall()
        except mysql.connector.errors.InterfaceError:
            # No results to fetch, return empty list
            pass
    
    def clear_cursor(self):
        """
        Safely clear any remaining results without raising exceptions.
        
        This ensures the cursor is ready for a new query.
        """
        try:
            # Try to consume any unread results
            while self.cursor.fetchall():
                # Continue until all results are consumed
                pass
        except mysql.connector.errors.InterfaceError:
            # This is expected if there are no results to fetch
            pass
        except Exception as e:
            # Handle any other unexpected errors
            print(f"Error clearing cursor: {e}")
    
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
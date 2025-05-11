from src.db_utils.DataBase import DataBase

database = DataBase()
database.connectToDatabase()

connection = database.getConnection()
cursor = database.getCursor()

def get_connection():
    """
    Get the database connection.
    """
    return connection

def get_cursor():
    """
    Get the database cursor.
    """
    return cursor

def close_connection():
    """
    Close the database connection.
    """
    if connection.is_connected():
        cursor.close()
        connection.commit()
        connection.close()
        print("MySQL connection is closed")
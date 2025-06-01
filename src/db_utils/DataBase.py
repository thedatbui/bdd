import mysql.connector


class DataBase:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connectToDatabase(self):
        """
        Connect to the MySQL database and return the connection object.
        """
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='dat',
                password='Alckart0246',
                database='InventaireRPG', 
                auth_plugin='mysql_native_password',
                use_pure=True,
                ssl_disabled=True
            )
            self.cursor = self.connection.cursor()
            print("Database connection established.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def closeConnection(self):
        """
        Close the database connection.
        """
        if self.connection:
            self.cursor.close()
            self.connection.commit()
            self.connection.close()
            print("Database connection closed.")
        else:
            print("No database connection to close.")

    def getConnection(self):
        """
        Get the current database connection.
        """
        if self.connection:
            return self.connection
        else:
            print("No database connection established.")
            return None
        
    def getCursor(self):
        """
        Get the current database cursor.
        """
        if self.cursor:
            return self.cursor
        else:
            print("No database cursor established.")
            return None
            
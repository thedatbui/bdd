import json
import csv
import mysql.connector
import re

def loadCSVfile(filePath):
    """
    Load a CSV file and return its contents as a list of dictionaries.
    Each dictionary represents a row in the CSV file, with the keys being the column headers.
    """
  
    with open(filePath, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


def loadJSONfile(filePath):
    """
    Load a JSON file and return its contents as a dictionary.
    """
    with open(filePath, mode='r', encoding='utf-8') as jsonfile:
        return json.load(jsonfile)

def checkInteger(value):
    """
    Check if the value is a valid integer.
    """
    try:
        int(value)
       
        if int(value) > 0:
            return True
        else:
            return False
    except ValueError:
        return False
    except TypeError:
        return False
   

def connectToDatabase():
    """
    Connect to the MySQL database and return the connection object.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='dat', # Create ur own user
            password='Alckart0246', # Create ur own password
            database='InventaireRPG', 
            auth_plugin='mysql_native_password',
            use_pure=True,
            ssl_disabled=True
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def loadPlayerData(cursor, playerFile):
     """
     Load player data from a CSV file into the database.
     """
     for player in playerFile:
        ID,userName,level,XP,Money,InventorySlot = (
            player['ID'], player['NomUtilisateur'],
            player['Niveau'], player['XP'], player['Monnaie'], player['SlotsInventaire']
        )

        # Check if the values are valid integers
        level = level if checkInteger(level) else None
        XP = XP if checkInteger(XP) else None
        Money = Money if checkInteger(Money) else None
        InventorySlot = InventorySlot if checkInteger(InventorySlot) else None
        ID = ID if checkInteger(ID) else None

    
        # # Check if player already exists
        cursor.execute("SELECT COUNT(*) FROM Player WHERE ID = %s OR UserName = %s", 
                    (player['ID'], player['NomUtilisateur']))
        
        if cursor.fetchone()[0] == 0 and level is not None and \
        XP is not None and Money is not None and InventorySlot is not None:
            # Only insert if player doesn't exist
            cursor.execute("INSERT INTO Player (ID, UserName, PlayerLevel, ExperiencePoints, WalletCredits, InventorySlot) " \
            "VALUES (%s, %s, %s, %s, %s, %s)", (ID, userName, \
            level, XP, Money, InventorySlot))
            print(f"Added player: {player['NomUtilisateur']}")

def extract_property_value(property_str):
    """
    Extract numeric value from a property string like 'Puissance d'attaque: 15'.
    Returns None if no number is found.
    """
    property = property_str.split(':')
    if len(property) > 1:
        if property[0] == 'Effet':
            # Extract the effect string
            return property[1].strip()
        elif property[0] == 'Puissance d\'attaque' or property[0] == 'Défense':
            return int(property[1].strip())
        else:  
            # Handle other properties if needed
            return property_str
    else:
        return property[0].strip()
        

def loadObjectData(cursor, objectFile):
    """
    Load object data from a CSV file into the database.
    """
    for object in objectFile:
        name, type_, properties, price = (
            object['Nom'], object['Type'], object['Propriétés'], object['Prix']
        )
        
        objectPrice = price if checkInteger(price) else None
        type_ = type_ if type_ in ['Arme', 'Armure', 'Potion', 'Artefact'] else None

        strength = 0
        Defence = 0
        effect = None
        # Extract properties
        if type_ == 'Arme' and type_ is not None:
            strength = extract_property_value(properties)
        elif type_ == 'Armure' and type_ is not None:
            Defence = extract_property_value(properties)
            if isinstance(Defence, str):
                # If the property is a string, we can assume it's an effect
                effect = Defence
                Defence = 0
        elif type_ == 'Potion' and type_ is not None:
            effect = extract_property_value(properties)
        elif type_ == 'Artefact' and type_ is not None:
            effect = extract_property_value(properties)

        # # Check if player already exists
        cursor.execute("SELECT COUNT(*) FROM Object WHERE ObjectName = %s", 
                    (name,))
    
        if cursor.fetchone()[0] == 0 and objectPrice is not None and type_ is not None:
            cursor.execute("INSERT INTO Object (ObjectName, Type, Strength, Defence, Effects, Price) " \
            "VALUES (%s, %s, %s, %s, %s, %s)", (name, type_, strength, Defence, effect, objectPrice))
            print(f"Added player: {object['Nom']}")


def main():
    """
    Main function to load data from CSV and JSON files into the database.
    """
    # Load CSV file
    playerFile = loadCSVfile('data/joueurs.csv')
    objectFile = loadCSVfile('data/objets.csv')
    spellsFile = loadCSVfile('data/sorts.csv')
    # Load JSON file
    charactersFile = loadJSONfile('data/personnages.json')
    npcFile = loadJSONfile('data/pnjs.json')


    # Connect to the database
    connection = connectToDatabase()
    if connection is None:
        print("Failed to connect to the database.")
        return
    cursor = connection.cursor()

    # Load player data to the database
    loadPlayerData(cursor, playerFile)

    # Load object data to the database
    loadObjectData(cursor, objectFile)
       
        
    # Fermer la connexion
    cursor.close()
    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()
import json
import csv
import xml.etree.ElementTree as ET
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


def loadXMLfile(filePath):
    """
    Load an XML file and return its contents as a dictionary.
    """
    tree = ET.parse(filePath)
    root = tree.getroot()
    data = {}
    
    for child in root:
        data[child.tag] = child.text
    
    return data
    

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
            user='hassan', # Create ur own user
            password='777', # Create ur own password
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
        ID,userName,level,XP,Money,InventorySlots = (
            player['ID'], player['NomUtilisateur'],
            player['Niveau'], player['XP'], player['Monnaie'], player['SlotsInventaire']
        )

        # Check if the values are valid integers
        level = level if checkInteger(level) else None
        XP = XP if checkInteger(XP) else None
        Money = Money if checkInteger(Money) else None
        InventorySlots = InventorySlots if checkInteger(InventorySlots) else None
        ID = ID if checkInteger(ID) else None

    
        # # Check if player already exists
        cursor.execute("SELECT COUNT(*) FROM Player WHERE ID = %s OR UserName = %s", 
                    (player['ID'], player['NomUtilisateur']))
        
        if cursor.fetchone()[0] == 0 and level is not None and \
        XP is not None and Money is not None and InventorySlots is not None:
            # Only insert if player doesn't exist
            cursor.execute("INSERT INTO Player (ID, UserName, PlayerLevel, ExperiencePoints, WalletCredits, InventorySlots) " \
            "VALUES (%s, %s, %s, %s, %s, %s)", (ID, userName, \
            level, XP, Money, InventorySlots))
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

def loadMonsterData(cursor, monsterFile):
    """
    Load monster data from an XML file into the database, including drops.
    """
    for monster in monsterFile['monstres']['monstre']:
        monster_id = int(monster['id'])
        name = monster['nom']
        attack = int(monster['attaque'])
        defense = int(monster['defense'])
        life_points = int(monster['vie'])

        # Check if the monster already exists
        cursor.execute("SELECT COUNT(*) FROM Bestiary WHERE ID = %s", (monster_id,))
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO Bestiary (ID, BeastName, Attack, Defence, LifePoints) "
                "VALUES (%s, %s, %s, %s, %s)",
                (monster_id, name, attack, defense, life_points)
            )
            print(f"Added monster: {name}")

        # Process drops
        if 'drops' in monster:
            for drop_name, drop_details in monster['drops'].items():
                if isinstance(drop_details, dict):
                    quantity = int(drop_details.get('nombre', 0))
                    probability = int(drop_details.get('probabilité', 0))

                    # Check if the drop already exists
                    cursor.execute(
                        "SELECT COUNT(*) FROM Rewards WHERE MonsterID = %s AND ObjectID = %s",
                        (monster_id, drop_name)
                    )
                    if cursor.fetchone()[0] == 0:
                        cursor.execute(
                            "INSERT INTO Rewards (MonsterID, ObjectID, DropRate) "
                            "VALUES (%s, %s, %s)",
                            (monster_id, drop_name, probability)
                        )
                        print(f"Added drop: {drop_name} for monster {name}")

def loadQuestData(cursor, questFile):
    """
    Load quest data from an XML file into the database.
    """
    for quest in questFile['quetes']['qu\u00eate']:
        name = quest['Nom']
        description = quest['Descripion']
        difficulty = int(quest['Difficult\u00e9'])
        experience = int(quest['Exp\u00e9rience'])
        gold_reward = int(quest['R\u00e9compenses']['Or']) if 'Or' in quest['R\u00e9compenses'] else 0

        # Check if the quest already exists
        cursor.execute("SELECT COUNT(*) FROM Quest WHERE QuestName = %s", (name,))
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO Quest (QuestName, Description, DifficultyLevel, RewardXP, RewardGold) "
                "VALUES (%s, %s, %s, %s, %s)",
                (name, description, difficulty, experience, gold_reward)
            )
            print(f"Added quest: {name}")

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

    # Load XML file
    monsterFile = loadXMLfile('data/monstres.xml')
    questFile = loadXMLfile('data/quetes.xml')
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
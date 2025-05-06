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
            cursor.execute("INSERT INTO Player (ID, UserName, PlayerLevel, ExperiencePoints, WalletCredits, InventorySlot) " \
            "VALUES (%s, %s, %s, %s, %s, %s)", (ID, userName, \
            level, XP, Money, InventorySlots))
            print(f"Added player: {player['NomUtilisateur']}")

def loadCharacterData(cursor, characters):
    """
    Load characters from JSON into the Character table.
    """
    classes_valides = [
        "Assassin", "Archer", "Barbare", "Berserker", "Chasseur",
        "Chevalier", "Démoniste", "Druide", "Enchanteresse", "Guerrier",
        "Illusionniste", "Mage", "Moine", "Nécromancien", "Paladin",
        "Prêtresse", "Rôdeur", "Sorcière", "Templier"
    ]

    corrections = {
        "R\u00f4deur": "Rôdeur",
        "D\u00e9moniste": "Démoniste",
        "Sorci\u00e8re": "Sorcière", 
        "N\u00e9cromancien" : "Nécromancien",  
        "Pr\u00eatresse" : "Prêtresse"
    }

    for c in characters:
        username = c["utilisateur"]

        # Chercher l’ID du joueur
        cursor.execute("SELECT ID FROM Player WHERE UserName = %s", (username,))
        result = cursor.fetchone()
        if not result:
            print(f"Utilisateur '{username}' non trouvé → personnage ignoré")
            continue
        player_id = result[0]

        char_name = c["Nom"]
        classe = c["Classe"].capitalize()

        # Correction si besoin
        classe = corrections.get(classe, classe)

        if classe not in classes_valides:
            print(f"Classe '{classe}' non valide pour {char_name} → ignoré")
            continue

        # Stats
        force = c["Force"]
        agi = c["Agilite"]
        intel = c["Intelligence"]
        hp = c["Vie"]
        mana = c["Mana"]

        # Insertion dans la table
        cursor.execute("""
            INSERT INTO `Character` (PlayerID, CharacterName, Class, Strength, Agility, Intelligence, pv, mana)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (player_id, char_name, classe, force, agi, intel, hp, mana))

        print(f"Ajouté : {char_name} → joueur {username}")

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
            if isinstance(strength, str):
                # If the property is a string, we can assume it's an effect
                effect = strength
                strength = 0
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

def load_spell_data(cursor, spells):
    """
    Load spell data from a CSV file into the database.
    """
    for s in spells:
        # Extraction brute des champs
        ID, Name, manacost, cd, power = (
            s['ID'],
            s['Name'],
            s['manacost'],
            s['cd'],
            s['power'],
        )

        # Validation des entiers
        ID       = ID if checkInteger(ID)       else None
        manacost = manacost if checkInteger(manacost) else None
        cd       = cd if checkInteger(cd)       else None
        power    = power if checkInteger(power) else None

        # On saute si un champ manque ou si le nom est vide
        if ID is None or manacost is None or cd is None or power is None or not Name:
            continue

        # Vérifier si le sort existe déjà
        cursor.execute(
            "SELECT COUNT(*) FROM Spell WHERE SpellID = %s",
            (ID,)
        )
        if cursor.fetchone()[0] == 0:
            # Insert unitaire
            cursor.execute(
                "INSERT INTO Spell (SpellID, Name, Power, ManaCost, Effect) "
                "VALUES (%s, %s, %s, %s, %s)",
                (ID, Name, power, manacost, cd)
            )
            print(f"Added spell: {Name}")

def insert_player(cursor, player):
    """
    character: dict avec les clés
      - CharacterID (int)  
      - PlayerID    (int)
      - ClassID     (int)
      - Name        (str)
      - Strength    (int)
      - Agility     (int)
      - Intelligence(int)
      - HitPoints   (int)
      - Mana        (int)
    """
    # Validation minimale
    required = ('ID','Name','Level','XP','Money','SlotsInventaire')
    if any(k not in player or player[k] is None for k in required):
        raise ValueError("Données incomplètes pour le personnage : " + ", ".join(required))
    
    sql = """
      INSERT INTO `Character`
        (CharacterID, PlayerID, ClassID, Name, Strength, Agility, Intelligence, HitPoints, Mana)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        int(player['ID']),
        player['Name'].strip(),
        int(player['Level']),
        int(player['XP']),
        int(player['Money']),
        int(player['SlotsInventaire']),
    )
    cursor.execute(sql, params)

def main():
    """
    Main function to load data from CSV and JSON files into the database.
    """
    # Load CSV file
    playerFile = loadCSVfile('data/joueurs.csv')
    objectFile = loadCSVfile('data/objets.csv')
    # spellsFile = loadCSVfile('bdd/data/sorts.csv')

    # # Load JSON file
    characters = loadJSONfile("data/personnages.json")["personnages"]
    # npcFile = loadJSONfile('bdd/data/pnjs.json')

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

    # Load Characters related to players
    loadCharacterData(cursor, characters)
    
    # Load object data to the database
    loadObjectData(cursor, objectFile)
    
    loadMonsterData(cursor, monsterFile)
    loadQuestData(cursor, questFile)
        
    # Fermer la connexion
    cursor.close()
    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()
from utils import *
  
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

def loadObjectData(cursor, objectFile):
    """
    Load object data from a CSV file into the database.
    """
    i = 0
    for object in objectFile:
        name, type_, properties, price, gold = (
            object['Nom'], object['Type'], object['Propriétés'], object['Prix'], 'Gold'
        )
        
        objectPrice = int(price) if checkInteger(price) else 0
        type_ = type_ if type_ in ['Arme', 'Armure', 'Potion', 'Artefact', 'Potions', 'Sword'] else None

        strength = 0
        Defence = 0
        effect = None
        
        cursor.execute("SELECT COUNT(*) FROM ObjectTest WHERE ObjectName = 'Gold'")
        if cursor.fetchone()[0] == 0:
            # Only insert if player doesn't exist
            cursor.execute("INSERT INTO ObjectTest (ObjectName) " \
            "VALUES (%s)", (gold,))
            print(f"Added object: {gold}")
        
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
        elif type_ == 'Potion' or type_ == 'Potions' and type_ is not None:
            effect = extract_property_value(properties)
        elif type_ == 'Artefact' and type_ is not None:
            effect = extract_property_value(properties)
        i += 1
        # # Check if player already exists
        cursor.execute("SELECT COUNT(*) FROM ObjectTest WHERE ObjectName = %s", 
                    (name,))

        if cursor.fetchone()[0] == 0 and type_ is not None:
            # Only insert if player doesn't exist
            cursor.execute("INSERT INTO ObjectTest (ObjectName, Type, Strength, Defence, Effects, Price) " \
            "VALUES (%s, %s, %s, %s, %s, %s)", (name,type_, strength, Defence, effect, objectPrice))
            print(f"Added object: {name}")
        else:
            print(f"Object {name} already exists in the database. Checking for updates...")
            # If the object already exists, check if the attributes are the same
            # check if the name is the same
            # check if the attributs are the same
            cursor.execute("SELECT Strength, Defence, Effects, Price FROM ObjectTest WHERE ObjectName = %s", 
                    (name,))
            result = cursor.fetchone()
            if result:
                db_strength, db_defence, db_effects, db_price = result
                if (strength != db_strength or Defence != db_defence or effect != db_effects or objectPrice != db_price):
                    cursor.execute("SELECT COUNT(*) FROM ObjectTest WHERE ObjectName = %s", 
                    (name + str(i),))
                    if cursor.fetchone()[0] == 0:
                    # add another object with the same name
                        cursor.execute("INSERT INTO ObjectTest (ObjectName, Type, Strength, Defence, Effects, Price) " \
                        "VALUES (%s, %s, %s, %s, %s, %s)", (name + str(i), type_, db_strength, db_defence, db_effects, db_price))
                        
                else:
                    print(f"Object {name} already exists with the same attributes. No update needed.")
             


def replace_underscores_with_spaces(text):
    """
    Replace underscores in a string with spaces.
    """
    final_text = ""
    alist = ['d', 'D', 'l', 'L']
    if isinstance(text, str):
        text = text.split('_')
        for i in text:
            if len(i) == 1 and i in alist:
                final_text += i + "'"
            else:
                final_text += i + " "
    return final_text.strip()
 


def loadMonsterData(cursor, root):
    """
    Load monster data from an XML file into the database, including drops.
    """
    #enlever les _ pour les objets
    
    print("Loading monster data...")
    for monster in root.findall('monstre'):
        monster_attaque = monster.find('attaque')
        monster_defense = monster.find('defense')
        monster_id = monster.find('id')
        monster_name = monster.find('nom')
        monster_vie = monster.find('vie')

        if monster_attaque is not None:
            monster_attaque = int(monster_attaque.text)
        if monster_defense is not None:
            monster_defense = int(monster_defense.text)
        if monster_id is not None:
            monster_id = int(monster_id.text) + 1
        if monster_name is not None:
            monster_name = monster_name.text
        if monster_vie is not None:
            monster_vie = int(monster_vie.text)
        
        # Vérifier que tous les champs nécessaires sont présents
        if monster_id is None or monster_name is None or monster_vie is None:
            print(f"Skipping monster with missing data: ID={monster_id}, Name={monster_name}, LifePoints={monster_vie}")
            continue

        # Insérer les données du monstre dans la table Bestiary
        cursor.execute(
            "SELECT COUNT(*) FROM Bestiary WHERE ID = %s",
            (monster_id,)
        )
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO Bestiary (ID, BeastName, Attack, Defence, LifePoints) "
                "VALUES (%s, %s, %s, %s, %s)",
                (monster_id, monster_name, monster_attaque, monster_defense, monster_vie)
            )
            print(f"Added monster: {monster_name}")

        # Vérifier que le monstre existe dans Bestiary avant d'insérer les drops
        cursor.execute(
            "SELECT COUNT(*) FROM Bestiary WHERE ID = %s",
            (monster_id,)
        )
        if cursor.fetchone()[0] == 0:
            print(f"Error: Monster with ID {monster_id} does not exist in Bestiary. Skipping drops.")
            continue

        # Process drops
     
        drops = monster.find('drops')
        for drop in drops:
            if replace_underscores_with_spaces(drop.tag) == 'Or':
                drop_name = 'Gold'
            else:
                drop_name = replace_underscores_with_spaces(drop.tag)
        
            drop_quantity = int(drop.find('nombre').text) if drop.find('nombre') is not None else 0
            drop_probability = int(drop.find('probabilité').text) if drop.find('probabilité') is not None else 0
                
            cursor.execute("SELECT COUNT(*) FROM ObjectTest WHERE ObjectName = %s", (drop_name,))

            if cursor.fetchone()[0] == 0:
                print(f"Warning: '{drop_name}' not found in ObjectTest. Skipping this drop.")
            else:
                # Check if the drop already exists for the monster
                cursor.execute(
                    "SELECT COUNT(*) FROM Rewards WHERE MonsterID = %s AND ObjectName = %s",
                    (monster_id, drop_name)
                )
                if cursor.fetchone()[0] > 0:
                    print(f"Drop '{drop_name}' already exists for monster ID {monster_id}. Skipping insert.")
                    continue
                # Insert drop data into the Rewards table
                cursor.execute(
                    "INSERT INTO Rewards (MonsterID, ObjectName, DropRate, Quantity) "
                    "VALUES (%s, %s, %s, %s)",
                    (monster_id, drop_name, drop_probability, drop_quantity)
                )
        
        
            print("1")
            print(f"Added drop: {drop_name} for monster: {monster_name}")
                
def loadQuestData(cursor, root):
    """
    Load quest data from an XML file into the database.
    """
    for quest in root.findall('quête'):
        quest_description = quest.find('Descripion').text
        quest_difficulty_level = int(quest.find('Difficulté').text)
        quest_name = quest.find('Nom').text
        quest_xp = int(quest.find('Expérience').text)
        
        # Insert quest data into the Quest table
        cursor.execute(
            "SELECT COUNT(*) FROM Quest WHERE Name = %s",
            (quest_name,)
        )
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO Quest (QuestName, Description, DifficultyLevel, RewardXP, ) "
                "VALUES (%s, %s, %s, %s)",
                (quest_name, quest_description, quest_difficulty_level, quest_xp)
            )
            print(f"Added quest: {quest_name}")
            
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


def loadCharacterData(cursor, characters):
    """
    Load characters from JSON into the Character table.
    """
    classes_valides = [
        "Assassin", "Archer", "Barbare", "Berserker", "Chasseur",
        "Chevalier", "Démoniste", "Druide", "Enchanteresse", "Guerrier",
        "Illusionniste", "Mage", "Moine", "Nécromancien", "Paladin",
        "Prêtresse", "Rôdeur", "Sorcière", "Templier", "Voleur"
    ]

    corrections = {
        "R\u00f4deur": "Rôdeur",
        "D\u00e9moniste": "Démoniste",
        "Sorci\u00e8re": "Sorcière", 
        "N\u00e9cromancien": "Nécromancien",  
        "Pr\u00eatresse": "Prêtresse",
        "Rodeur": "Rôdeur",  # En cas de faute sans accent
        "Pretresse": "Prêtresse",
        "Necromancien": "Nécromancien"
    }

    for c in characters:
        username = c.get("utilisateur")
        char_name = c.get("Nom")
        raw_class = c.get("Classe", "").strip()

        # Correction d'encodage et orthographe
        classe = corrections.get(raw_class, raw_class)

        # Vérification de la validité de la classe
        if classe not in classes_valides:
            print(f"❌ Classe '{classe}' non valide pour {char_name} → ignoré")
            continue

        # Récupération du joueur
        cursor.execute("SELECT ID FROM Player WHERE UserName = %s", (username,))
        result = cursor.fetchone()
        if not result:
            print(f"❌ Utilisateur '{username}' non trouvé → personnage ignoré")
            continue
        player_id = result[0]

        # Stats
        force = c.get("Force", 0)
        agi = c.get("Agilite", 0)
        intel = c.get("Intelligence", 0)
        hp = c.get("Vie", 0)
        mana = c.get("Mana", 0)

        # Insertion
        try:
            cursor.execute("""
                INSERT INTO `Character` (PlayerID, CharacterName, Class, Strength, Agility, Intelligence, pv, mana)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (player_id, char_name, classe, force, agi, intel, hp, mana))
            print(f"✅ Ajouté : {char_name} ({classe}) → joueur {username}")
        except Exception as e:
            print(f"⚠️ Erreur à l'insertion de '{char_name}' : {e}")

def main():
    """
    Main function to load data from CSV and JSON files into the database.
    """
    # Load CSV file
    playerFile = loadCSVfile('data/joueurs.csv')
    objectFile = loadCSVfile('data/objets.csv')
    # spellsFile = loadCSVfile('bdd/data/sorts.csv')

    # # Load JSON file
    charactersFile = loadJSONfile('data/personnages.json')
    characters = charactersFile["personnages"]
    # npcFile = loadJSONfile('data/pnjs.json')

    # Load XML file
    monsterFile = loadXMLfile('data/monstres.xml')
    monsterFile = loadXMLfile('data/monstres.xml')
    # questFile = loadXMLfile('data/quetes.xml')

    # Connect to the database
    connection = connectToDatabase()
    if connection is None:
        print("Failed to connect to the database.")
        return
    cursor = connection.cursor()

    # Load player data to the database
    loadPlayerData(cursor, playerFile)

    # # Load object data to the database
    loadObjectData(cursor, objectFile)
    
    loadMonsterData(cursor, monsterFile)

    # Load Characters related to players
    loadCharacterData(cursor, characters)

    #loadQuestData(cursor, questFile)
        
    # Fermer la connexion
    cursor.close()
    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()
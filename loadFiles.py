from utils_loadFiles import *
from src.db_utils.connectToDataBase import *

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
        
        # Check if player already exists
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
             
def loadMonsterData(cursor, root):
    """
    Load monster data from an XML file into the database, including drops.
    """
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
                # Gérer l'or séparément
                gold_amount = int(drop.find('nombre').text) if drop.find('nombre') is not None else 0
                gold_probability = int(drop.find('probabilité').text) if drop.find('probabilité') is not None else 0
                
                # Insérer l'or dans la table MonsterGold
                cursor.execute(
                    "INSERT INTO MonsterGold (MonsterID, GoldAmount, DropRate) "
                    "VALUES (%s, %s, %s)",
                    (monster_id, gold_amount, gold_probability)
                )
                print(f"Added gold drop: {gold_amount} (rate: {gold_probability}%) for monster: {monster_name}")
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

        # Vérifie si une quête identique existe déjà (même nom + mêmes caractéristiques)
        cursor.execute(
            "SELECT ID FROM Quest WHERE QuestName = %s AND Description = %s AND DifficultyLevel = %s AND RewardXP = %s",
            (quest_name, quest_description, quest_difficulty_level, quest_xp)
        )
        quest_row = cursor.fetchone()

        # Si elle n'existe pas, on l'insère
        if not quest_row:
            cursor.execute(
                "INSERT INTO Quest (QuestName, Description, DifficultyLevel, RewardXP) "
                "VALUES (%s, %s, %s, %s)",
                (quest_name, quest_description, quest_difficulty_level, quest_xp)
            )
            print(f"Added quest: {quest_name} (Diff {quest_difficulty_level}, XP {quest_xp})")
            quest_id = cursor.lastrowid
        else:
            quest_id = quest_row[0]

        # Gestion des récompenses
        rewards = quest.find('Récompenses')
        if rewards is not None:
            for reward in rewards:
                if reward.tag == 'Or':
                    # Gérer l'or séparément
                    gold_amount = int(reward.text)
                    cursor.execute(
                        "INSERT INTO QuestGold (QuestID, GoldAmount) "
                        "VALUES (%s, %s)",
                        (quest_id, gold_amount)
                    )
                    print(f"Added gold reward: {gold_amount} for quest: {quest_name}")
                else:
                    reward_name = reward.text
                    reward_quantity = 1

                    cursor.execute("SELECT COUNT(*) FROM ObjectTest WHERE ObjectName = %s", (reward_name,))
                    if cursor.fetchone()[0] == 0:
                        print(f"Warning: '{reward_name}' not found in ObjectTest. Skipping this reward.")
                    else:
                        cursor.execute(
                            "SELECT COUNT(*) FROM Quest_Objects WHERE QuestID = %s AND ObjectName = %s",
                            (quest_id, reward_name)
                        )
                        if cursor.fetchone()[0] > 0:
                            print(f"Reward '{reward_name}' already exists for quest '{quest_name}'. Skipping insert.")
                            continue

                        cursor.execute(
                            "INSERT INTO Quest_Objects (QuestID, ObjectName, Quantity) "
                            "VALUES (%s, %s, %s)",
                            (quest_id, reward_name, reward_quantity)
                        )
                        print(f"Added reward: {reward_name} for quest: {quest_name}")

    
            
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

def to_int(value):
    """
    Convertit une valeur en entier. Si la conversion échoue, retourne 0.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

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

        force = to_int(c.get("Force"))
        agi = to_int(c.get("Agilite"))
        intel = to_int(c.get("Intelligence"))
        hp = to_int(c.get("Vie"))
        mana = to_int(c.get("Mana"))


        # Insertion
        try:
            cursor.execute("""
                INSERT INTO CharacterTable (PlayerID, CharacterName, Class, Strength, Agility, Intelligence, pv, mana)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (player_id, char_name, classe, force, agi, intel, hp, mana))
            print(f"✅ Ajouté : {char_name} ({classe}) → joueur {username}")
        except Exception as e:
            print(f"⚠️ Erreur à l'insertion de '{char_name}' : {e}")


def loadNpcData(cursor, npcFile):
    """
    Load NPCs from a JSON file into the NPC table & other related tables 
    """
    npcs = npcFile  

    for npc in npcs:
        full_name = npc.get("Nom", "").strip()
        dialogue = npc.get("Dialogue", "").strip()

        if not full_name:
            print("⚠️ PNJ sans nom trouvé → ignoré")
            continue

        # Séparer le nom et le type si une virgule est présente
        if "," in full_name:
            name, pnj_type = [part.strip() for part in full_name.split(",", 1)]
        else:
            name = full_name
            pnj_type = "Inconnu"

        # Vérifie si le PNJ existe déjà
        cursor.execute("SELECT ID FROM NPC WHERE NpcName = %s", (name,))
        result = cursor.fetchone()
        if result:
            print(f"PNJ déjà présent : {name}")
            npc_id = result[0]
        else:
            cursor.execute("INSERT INTO NPC (NpcName, Dialogue, Type) VALUES (%s, %s, %s)", (name, dialogue, pnj_type))
            npc_id = cursor.lastrowid
            print(f"✅ Ajouté PNJ : {name}")
        
        # Chargement des quêtes proposées
        for quest_name in npc.get("Quêtes", []):
            # Vérifier si la relation existe déjà
            cursor.execute("SELECT COUNT(*) FROM NPCQuest WHERE NPCID = %s AND QuestName = %s", (npc_id, quest_name))
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO NPCQuest (NPCID, QuestName) VALUES (%s, %s)", (npc_id, quest_name))
                print(f"✅ Ajoutée quête '{quest_name}' pour PNJ '{name}'")

        # Chargement de l'inventaire
        objets_vus = {}
        for item in npc.get("Inventaire", []):
            objet = item.strip()

            if not objet:
                continue
            objets_vus[objet] = objets_vus.get(objet, 0) + 1

        for objet, quantite in objets_vus.items():
            try:
                # Vérifie si l'objet existe dans ObjectTest
                cursor.execute("SELECT COUNT(*) FROM ObjectTest WHERE ObjectName = %s", (objet,))
                if cursor.fetchone()[0] == 0:
                    print(f"⚠️ Objet inconnu '{objet}' → ignoré pour PNJ '{name}'")
                    continue

                # Insère l'objet et la quantité
                cursor.execute("""
                    INSERT INTO NPCInventory (NPCID, ObjectName, Quantity)
                    VALUES (%s, %s, %s)
                """, (npc_id, objet, quantite))
                print(f"✅ Ajouté objet '{objet}' ×{quantite} pour PNJ '{name}'")

            except Exception as e:
                print(f"⚠️ Erreur ajout objet '{objet}' pour PNJ '{name}' : {e}")


        

def main():
    """
    Main function to load data from CSV and JSON files into the database.
    """
    # Load CSV file
    playerFile = loadCSVfile('data/joueurs.csv')
    objectFile = loadCSVfile('data/objets.csv')
    # spellsFile = loadCSVfile('bdd/data/sorts.csv')

    # Load JSON file
    charactersFile = loadJSONfile('data/personnages.json')
    characters = charactersFile["personnages"]
    npcFile = loadJSONfile('data/pnjs.json')
    NPCs = npcFile["PNJs"]
    
    # Load XML file
    monsterFile = loadXMLfile('data/monstres.xml')
    monsterFile = loadXMLfile('data/monstres.xml')
    questFile = loadXMLfile('data/quetes.xml')

    # Connect to the database
    cursor = get_cursor()
    
    # Load player data to the database
    loadPlayerData(cursor, playerFile)

    # # Load object data to the database
    loadObjectData(cursor, objectFile)
    
    loadMonsterData(cursor, monsterFile)

    # Load Characters related to players
    loadCharacterData(cursor, characters)

    # Load NPC data
    loadNpcData(cursor, NPCs)
    
    loadQuestData(cursor, questFile)
        
    # Fermer la connexion
    close_connection()

if __name__ == "__main__":
    main()
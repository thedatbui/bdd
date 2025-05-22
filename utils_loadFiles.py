import csv
import json
import xml.etree.ElementTree as ET

def loadCSVfile(filePath):
    """
    Load a CSV file and return its contents as a list of dictionaries.
    Each dictionary represents a row in the CSV file, with the keys being the column headers.
    Raises an exception if the file can't be read or parsed.
    """
    try:
        with open(filePath, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]
    except Exception as e:
        raise RuntimeError(f"Erreur lors du chargement du fichier CSV '{filePath}' : {e}")

def loadJSONfile(filePath):
    """
    Load a JSON file and return its contents as a dictionary.
    Raises an exception if the file can't be read or parsed.
    """
    try:
        with open(filePath, mode='r', encoding='utf-8') as jsonfile:
            return json.load(jsonfile)
    except Exception as e:
        raise RuntimeError(f"Erreur lors du chargement du fichier JSON '{filePath}' : {e}")

def loadXMLfile(filePath):
    """
    Load an XML file and return its root element.
    Raises an exception if the file can't be read or parsed.
    """
    try:
        tree = ET.parse(filePath)
        return tree.getroot()
    except Exception as e:
        raise RuntimeError(f"Erreur lors du chargement du fichier XML '{filePath}' : {e}")

    
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
    except AttributeError:
        return False
   

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
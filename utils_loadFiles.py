import json
import csv
import xml.etree.ElementTree as ET

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
    Load an XML file and return its root element.
    """
    tree = ET.parse(filePath)
    return tree.getroot()

    
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
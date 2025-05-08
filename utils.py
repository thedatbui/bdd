from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt
import json
import csv
import xml.etree.ElementTree as ET
import mysql.connector

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
   
def connectToDatabase():
    """
    Connect to the MySQL database and return the connection object.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='dat',
            password='Alckart0246',
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

def setupButtons(mainLayout, *button_texts):
    """Create buttons and add them to a layout within mainLayout"""
    layout = QHBoxLayout()
    layout.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
    buttons = []
    
    for text in button_texts:
        button = QPushButton(text)
        button.setFixedSize(200, 50)
        button.setStyleSheet("background-color: lightblue; font-size: 16px;")
        layout.addWidget(button)
        buttons.append(button)
    
    mainLayout.addLayout(layout)
    return buttons if len(buttons) > 1 else buttons[0]


def setupVButtons(mainLayout, *button_texts):
    """Create buttons and add them to a layout within mainLayout"""
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
    buttons = []
    
    for text in button_texts:
        button = QPushButton(text)
        button.setFixedSize(200, 50)
        button.setStyleSheet("background-color: lightblue; font-size: 16px;")
        layout.addWidget(button)
        buttons.append(button)
    
    mainLayout.addLayout(layout)
    return buttons if len(buttons) > 1 else buttons[0]

def setupLabel(mainLayout, *text):
    """
    Create a label with the specified text and add it to the given layout.
    """
    layout = QHBoxLayout()
    for text in text:
        label = QLabel(text)
        label.setStyleSheet("font-size: 16px;")
        layout.addWidget(label)

    mainLayout.addLayout(layout)
    return label

def setupLineEdit(mainLayout, *labelText):
    """
    Create a line edit with the specified placeholder text and add it to the given layout.
    """
    layout = QHBoxLayout()
    lineEdits = []
    for text in labelText:
        label = QLabel(text)
        lineEdit = QtWidgets.QLineEdit()
        lineEdits.append(lineEdit)
        lineEdit.setStyleSheet("font-size: 16px;")
        layout.addWidget(label)
        layout.addWidget(lineEdit)

    mainLayout.addLayout(layout)
    return lineEdits if len(lineEdits) > 1 else lineEdits[0]
    

def clear_screen(mainLayout):
    """Remove all widgets from the main layout"""
    for i in reversed(range(mainLayout.count())):
        item = mainLayout.itemAt(i)
        if item.widget():
            item.widget().deleteLater()
        elif item.layout():
            nested_layout = item.layout()
            for j in reversed(range(nested_layout.count())):
                nested_item = nested_layout.itemAt(j)
                if nested_item.widget():
                    nested_item.widget().deleteLater()
            mainLayout.removeItem(item)
        elif item.spacerItem():
            mainLayout.removeItem(item)

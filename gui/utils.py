import xml.etree.ElementTree as ET
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QScrollArea, QLineEdit, QMessageBox, QMenu
from PyQt5.QtCore import Qt

currentMenuState = 0
currentUser = None
MenuState = {
    "IntroMenu": 0,
    "LogIn": 1,
    "Create Account": 2,
    "Main Menu": 3,
    "Character": 4,
    "Inventory": 5,
    "Npc": 6,
    "Bestiary": 7,
    "Profile": 8,
}

def getCurrentUser():
    """
    Get the current user.
    """
    return currentUser

def setCurrentUser(user):
    """
    Set the current user.
    """
    global currentUser
    currentUser = user
    print(f"Current user set to: {currentUser.getName() if currentUser else 'None'}")
                                  
def getMenuState():
    """
    Get the current menu state.
    """
    return currentMenuState

def setMenuState(state):
    """
    Set the current menu state.
    """
    global currentMenuState
    currentMenuState = MenuState[state]
    print(f"Current menu state: {currentMenuState}")
    
def setupButtons(mainLayout, size, *button_texts):
    """Create buttons and add them to a layout within mainLayout"""
    layout = QHBoxLayout()
    layout.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
    buttons = []
    
    for text in button_texts:
        button = QPushButton(text)
        button.setFixedSize(size[0], size[1])
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
    labels = []
    for text in text:
        label = QLabel(text)
        label.setStyleSheet("font-size: 16px;")
        layout.addWidget(label)
        labels.append(label)
    
    mainLayout.addLayout(layout)
    return labels if len(labels) > 1 else labels[0]
    
def setupVLabel(mainLayout, *text):
    """
    Create a label with the specified text and add it to the given layout.
    """
    layout = QVBoxLayout()
    labels = []
    for text in text:
        label = QLabel(text)
        label.setStyleSheet("font-size: 16px;")
        layout.addWidget(label)
        labels.append(label)
    
    mainLayout.addLayout(layout)
    return labels if len(labels) > 1 else labels[0]


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
    

def clear_screen(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)  # détache le widget du layout et le détruit
        else:
            # Si c'est un sous-layout (layout imbriqué)
            sub_layout = item.layout()
            if sub_layout is not None:
                clear_screen(sub_layout)
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt
import sys
from loadFiles import *

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

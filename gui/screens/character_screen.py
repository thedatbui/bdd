from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt

from gui.components.labels import create_title_label, create_label
from gui.components.inputs import *
from gui.components.butttons import *
from gui.service.player_service import *
from gui.service.character_service import *
from gui.utils import *
from gui.models.Character import Character

class CharacterMenuScreen:
    """
    The character menu screen of the application.
    This class sets up the character menu screen and its components.
    """

    def __init__(self, main_window, scene_manager):
        """
        Initialize the character menu screen.

        Args:
            main_window: The application's main window
            scene_manager: The scene manager to handle screen transitions
        """
        self.main_window = main_window
        self.scene_manager = scene_manager
        self.main_layout = main_window.mainLayout
        self.player_service = PlayerService()
        self.db = DatabaseService()
        self.character_service = CharacterService()
    

    def setupCharacterMenu(self):
        """
        Set up the character menu with a scrollable list of characters.
        """
        clear_screen(self.main_layout)
        self.currentUser = self.main_window.current_user
        # Header
        self.label = create_title_label(f"Choose Your Character {self.currentUser.getName()} !")
        self.main_layout.addWidget(self.label)

        # Fetch characters from database
        self.characterList = self.currentUser.getCharacterFromDatabase()

        # Create list widget
        self.characterListLayout = QHBoxLayout()
        self.character_list = QtWidgets.QListWidget()
        # if the character name is already in the list, it will not be added again
        for character in self.characterList:
            if character.name not in [item.text() for item in self.character_list.findItems("", QtCore.Qt.MatchContains)]:
                item = QtWidgets.QListWidgetItem(character.name)
                self.character_list.addItem(item)
        self.characterListLayout.addWidget(self.character_list)
        
        # Enable context menu and double-click selection
        self.character_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.character_list.customContextMenuRequested.connect(self.showCharacterContextMenu)
        self.character_list.itemDoubleClicked.connect(self.selectCharacter)

        self.character_details = create_label("Character Details", 10, "blue", Qt.AlignTop | Qt.AlignLeft)
        self.characterListLayout.addWidget(self.character_details)

        self.character_list.currentItemChanged.connect(self.on_item_changed)
        
        self.main_layout.addLayout(self.characterListLayout)
        self.buttonList = add_horizontal_buttons(self.main_layout, (200, 50), "Create Character", "Back")
        self.buttonList[0].clicked.connect(self.setupCreateCharacterMenu)
        self.buttonList[1].clicked.connect(lambda: self.scene_manager.switch_to_menu("Main Menu"))
       
    def showCharacterContextMenu(self, position):
        """
        Show context menu for character list items.
        """
        menu = QMenu()
        delete_action = menu.addAction("Delete Character")
        
        action = menu.exec_(self.character_list.mapToGlobal(position))
        
        if action == delete_action:
            self.deleteSelectedCharacter()

    def deleteSelectedCharacter(self):
        """
        Delete the currently selected character.
        """
        current_row = self.character_list.currentRow()
        if current_row >= 0:
            character = self.characterList[current_row]
            
            # Confirm deletion
            confirm = QMessageBox.question(
                self.main_window,
                "Confirm Deletion",
                f"Are you sure you want to delete character '{character.name}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if confirm == QMessageBox.Yes:
                try:
                    # Remove from list
                    self.character_list.takeItem(current_row)
                    self.character_service.delete_character(character.Id, self.currentUser.getId())
                    self.currentUser.setCharacterSelected(None)
                    QMessageBox.information(
                        self.main_window,
                        "Success",
                        f"Character '{character.name}' has been deleted."
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self.main_window,
                        "Error",
                        f"Failed to delete character: {str(e)}"
                    )

    def selectCharacter(self, item):
        """
        Select the character when double-clicked.
        """
        current_row = self.character_list.currentRow()
        if current_row >= 0:
            character = self.characterList[current_row]
            self.currentUser.setCharacterSelected(character)
            
            QMessageBox.information(
                self.main_window,
                "Character Selected",
                f"You have selected '{character.name}' as your active character."
            )
            
            # Update character name in main menu
            self.scene_manager.switch_to_menu("Main Menu")
        
    def on_item_changed(self, current, previous):
        """
        Update the character details when an item is selected in the list.
        """
        if current:
            character = self.characterList[self.character_list.currentRow()]
            self.character_details.setText(f"""Character Details:
        Class: {character.getAttribute('classe')}
        Strength: {character.getAttribute('strength')}
        Agility: {character.getAttribute('agility')}
        Intelligence: {character.getAttribute('intelligence')}
        PV: {character.getAttribute('pv')}
        Mana: {character.getAttribute('mana')}""")

    def setupManageAttributesMenu(self):
        """
        Set up the manage attributes menu.
        """
        current_row = self.character_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self.main_window, "Error", "Please select a character first!")
            return

        character = self.characterList[current_row]
        available_points = self.character_service.get_attribute_points(character.Id)
        
        if available_points <= 0:
            QMessageBox.information(self.main_window, "No Points Available", "You don't have any attribute points to distribute!")
            return

        clear_screen(self.main_layout)

        self.label = create_title_label(f"Manage Attributes - {character.name}")
        self.main_layout.addWidget(self.label)

        # Add attribute points display
        self.attributePointsLabel = QLabel(f"Attribute Points Available: {available_points}")
        self.attributePointsLabel.setStyleSheet("color: green; font-weight: bold;")
        self.main_layout.addWidget(self.attributePointsLabel)
        
        # Initialize attribute values
        self.attributes = {
            "Strength": character.getAttribute("strength"),
            "Agility": character.getAttribute("agility"),
            "Intelligence": character.getAttribute("intelligence"),
            "pv": character.getAttribute("pv"),
            "mana": character.getAttribute("mana")
        }
        
        # Create layouts for attributes with increase/decrease buttons
        self.attributeLayouts = {}
        for attr in self.attributes:
            layout = QHBoxLayout()
            
            # Label showing attribute name and current value
            label = QLabel(f"{attr}: {self.attributes[attr]}")
            layout.addWidget(label)
            layout.addStretch()
            
            # Only add +/- buttons for Strength, Agility, and Intelligence
            if attr in ["Strength", "Agility", "Intelligence"]:
                self.buttonList = add_horizontal_buttons(layout, (30, 30), "-", "+")
                decreaseBtn = self.buttonList[0]
                increaseBtn = self.buttonList[1]
                
                decreaseBtn.clicked.connect(lambda checked, a=attr: self.decreaseAttribute(a))
                increaseBtn.clicked.connect(lambda checked, a=attr: self.increaseAttribute(a))
            else:
                # For pv and mana, just show the value
                layout.addStretch()
        
            # Store references to the label for updating
            self.attributeLayouts[attr] = {
                "layout": layout,
                "label": label
            }
            
            # Add the attribute layout to main layout
            self.main_layout.addLayout(layout)
        
        self.main_layout.addStretch(1)

        self.buttonList = add_horizontal_buttons(self.main_layout, (200, 50), "Save Changes", "Back")
        save_button = self.buttonList[0]
        back_button = self.buttonList[1]

        # Connect each button to its appropriate function
        back_button.clicked.connect(self.setupCharacterMenu)
        save_button.clicked.connect(lambda: self.saveAttributeChanges(character))

    def saveAttributeChanges(self, character):
        """
        Save the changes made to character attributes.
        """
        # Check if all points have been used
        current_points = int(self.attributePointsLabel.text().split(": ")[1])
        if current_points > 0:
            QMessageBox.warning(self.main_window, "Error", f"You still have {current_points} points to distribute!")
            return

        # Update character attributes in database
        query = """
        UPDATE CharacterTable 
        SET Strength = %s, Agility = %s, Intelligence = %s
        WHERE ID = %s
        """
        values = (
            self.attributes["Strength"],
            self.attributes["Agility"],
            self.attributes["Intelligence"],
            character.Id
        )
        
        if self.character_service.db_service.execute_query(query, values):
            if self.character_service.db_service.commit():
                QMessageBox.information(self.main_window, "Success", "Character attributes updated successfully!")
                self.setupCharacterMenu()
            else:
                QMessageBox.warning(self.main_window, "Error", "Failed to save changes!")
        else:
            QMessageBox.warning(self.main_window, "Error", "Failed to update character attributes!")

    def setupCreateCharacterMenu(self):
        """
        Set up the create character menu.
        """
        clear_screen(self.main_layout)

        self.label = create_title_label(f"Create your character {self.currentUser.getName()} !")
        self.main_layout.addWidget(self.label)

        self.inputField = create_line_edit("Enter your character name")
        self.inputField.returnPressed.connect(lambda: self.on_input_submitted(self.inputField))
        self.main_layout.addWidget(self.inputField)

        self.classLayout = QHBoxLayout()
        self.classeCombobox = QtWidgets.QComboBox()
        self.classeCombobox.addItems(["Assassin", "Archer", "Barbare", "Berserker", "Chasseur","Chevalier", "Démoniste", "Druide", 
                                    "Enchanteresse", "Guerrier","Illusionniste", "Mage", "Moine", "Nécromancien", "Paladin","Prêtresse", "Rôdeur", "Sorcière", "Templier"])
        self.classeLabel = QLabel("Choose your class: ")
        self.classLayout.addWidget(self.classeLabel)
        self.classLayout.addWidget(self.classeCombobox)
        self.main_layout.addLayout(self.classLayout)
        
        # Initialize attribute values
        self.attributes = {
            "Strength": 10,
            "Agility": 10,
            "Intelligence": 10,
            "pv": 100,
            "mana": 100
        }
        
        # Add attribute points display
        self.attributePointsLabel = QLabel("Attribute Points Available: 5")
        self.attributePointsLabel.setStyleSheet("color: green; font-weight: bold;")
        self.main_layout.addWidget(self.attributePointsLabel)
        
        # Create layouts for attributes with increase/decrease buttons
        self.attributeLayouts = {}
        for attr in self.attributes:
            layout = QHBoxLayout()
            
            # Label showing attribute name and current value
            label = QLabel(f"{attr}: {self.attributes[attr]}")
            layout.addWidget(label)
            layout.addStretch()
            
            # Only add +/- buttons for Strength, Agility, and Intelligence
            if attr in ["Strength", "Agility", "Intelligence"]:
                self.buttonList = add_horizontal_buttons(layout, (30, 30), "-", "+")
                decreaseBtn = self.buttonList[0]
                increaseBtn = self.buttonList[1]
                
                decreaseBtn.clicked.connect(lambda checked, a=attr: self.decreaseAttribute(a))
                increaseBtn.clicked.connect(lambda checked, a=attr: self.increaseAttribute(a))
            else:
                # For pv and mana, just show the value
                layout.addStretch()
        
            # Store references to the label for updating
            self.attributeLayouts[attr] = {
                "layout": layout,
                "label": label
            }
            
            # Add the attribute layout to main layout
            self.main_layout.addLayout(layout)
        
        self.main_layout.addStretch(1)

        self.buttonList = add_horizontal_buttons(self.main_layout, (200, 50), "Create Character", "Back")
        createAcc_button = self.buttonList[0]
        back_button = self.buttonList[1]

        # Connect each button to its appropriate function
        back_button.clicked.connect(self.setupCharacterMenu)
        createAcc_button.clicked.connect(self.createCharacter)

    def increaseAttribute(self, attr):
        """Increase the attribute value if points are available"""
        # Check if we have points available
        current_points = int(self.attributePointsLabel.text().split(": ")[1])
        if current_points > 0:
            self.attributes[attr] += 1
            self.attributeLayouts[attr]["label"].setText(f"{attr}: {self.attributes[attr]}")
            self.attributePointsLabel.setText(f"Attribute Points Available: {current_points - 1}")

    def decreaseAttribute(self, attr):
        """Decrease the attribute value and return the point"""
        if self.attributes[attr] > 10:  # Don't go below base value
            self.attributes[attr] -= 1
            self.attributeLayouts[attr]["label"].setText(f"{attr}: {self.attributes[attr]}")
            current_points = int(self.attributePointsLabel.text().split(": ")[1])
            self.attributePointsLabel.setText(f"Attribute Points Available: {current_points + 1}")

    def createCharacter(self):
        """Handle character creation"""
        characterName = self.inputField.text()
        classe = self.classeCombobox.currentText()
        if not characterName:
            QMessageBox.warning(self.main_window, "Input Error", "Please enter a character name.")
            return

        # Check if the character name already exists
        result = self.character_service.check_character_exists(characterName)
        if result:
            QMessageBox.warning(self.main_window, "Input Error", f"Character {characterName} already exists.")
            self.inputField.clear()
            self.inputField.setFocus()
            return

        # Check if all attribute points have been used
        current_points = int(self.attributePointsLabel.text().split(": ")[1])
        if current_points > 0:
            QMessageBox.warning(self.main_window, "Input Error", f"You still have {current_points} attribute points to distribute.")
            return

        # Create a new Character object
        newCharacter = Character(None, characterName, classe, self.attributes["Strength"], self.attributes["Agility"], 
                                 self.attributes["Intelligence"], self.attributes["pv"], self.attributes["mana"])

        # Insert the new character into the database
        success, message = self.character_service.create_character(self.currentUser.getId(), newCharacter)
        
        if success:
            QMessageBox.information(self.main_window, "Success", message)
            self.scene_manager.switch_to_menu("Character")
        else:
            QMessageBox.warning(self.main_window, "Error", message)
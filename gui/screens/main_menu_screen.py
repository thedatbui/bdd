from PyQt5.QtWidgets import QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import Qt

from gui.components.labels import *
from gui.components.butttons import *
from gui.utils import *
from gui.service.player_service import PlayerService
from gui.service.character_service import CharacterService

class MainMenuScreen:
    def __init__(self, main_window, scene_manager):
        """
        Initialize the main menu screen.
        
        Args:
            main_window: The application's main window
            scene_manager: The scene manager to handle screen transitions
        """
        self.main_window = main_window
        self.scene_manager = scene_manager
        self.main_layout = main_window.mainLayout
        self.player_service = PlayerService()
        self.character_service = CharacterService()
        
    
    def setupMainMenu(self):
        """
        Set up the main menu layout.
        """
        clear_screen(self.main_layout)
        self.currentUser = self.main_window.current_user
        self.character = self.currentUser.getCharacterSelected()
        
        # Récupérer les informations à jour depuis la base de données
        player_info = self.player_service.get_player_by_username(self.currentUser.getName())
        if player_info:
            self.currentUser.setLevel(player_info.getLevel())
            self.currentUser.setMoney(player_info.getMoney())
            self.currentUser.setInventorySlot(player_info.getInventorySlot())
        
        self.label = create_title_label(f"Welcome back {self.currentUser.getName()} !")
        self.main_layout.addWidget(self.label)
        
        self.testLayout = add_horizontal_labels(self.main_layout, "ID: ", "Money: ", "level: ", "Character: ")
        self.idLabel = self.testLayout[0]
        self.idLabel.setText(f"ID: {self.currentUser.getId()}")
        self.moneyLabel = self.testLayout[1]
        self.moneyLabel.setText(f"Money: {self.currentUser.getMoney()}")
        self.levelLabel = self.testLayout[3]
        self.levelLabel.setText(f"Level: {self.currentUser.getLevel()}")
        self.characterLabel = self.testLayout[2]
        self.characterLabel.setText(f"Character: {self.currentUser.getCharacterSelected().getAttribute('name') if self.currentUser.getCharacterSelected() else 'None'}")

        self.questLayout = add_horizontal_labels(self.main_layout, "Quest: ", "XP: ")
        self.QuestLabel = self.questLayout[0]
        self.XPLabel = self.questLayout[1]
        self.XPLabel.setText(f"XP: {self.currentUser.getXp()}")

        if self.character is None:
            self.QuestLabel.setText("Quest: None")
        else:
            self.charaterId = self.character.getAttribute("Id")
            self.QuestLabel.setText(f"Quest: {self.character_service.get_selected_quest(self.charaterId) if self.character_service.get_selected_quest(self.charaterId) else 'None'}")
        self.main_layout.addStretch(1)

        self.buttonLayout = add_vertical_buttons(self.main_layout, (200, 50),"Character", "Inventory", "NPC", "Monster", "Quest", "Manage Attributes", "Profile")
        
        character_button = self.buttonLayout[0]
        inventory_button = self.buttonLayout[1]
        npc_button = self.buttonLayout[2]
        monster_button = self.buttonLayout[3]
        quest_button = self.buttonLayout[4]
        manage_attributes_button = self.buttonLayout[5]
        profile_button = self.buttonLayout[6]

        self.main_layout.addStretch(1)
        #Connect each button to its appropriate function
        character_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("Character"))
        if self.currentUser.getCharacterSelected() is None:
            inventory_button.setEnabled(False)
            inventory_button.setStyleSheet("background-color: gray;")
            npc_button.setEnabled(False)
            npc_button.setStyleSheet("background-color: gray;")
            monster_button.setEnabled(False)
            monster_button.setStyleSheet("background-color: gray;")
            quest_button.setEnabled(False)
            quest_button.setStyleSheet("background-color: gray;")
            manage_attributes_button.setEnabled(False)
            manage_attributes_button.setStyleSheet("background-color: gray;")
        else:
            inventory_button.setEnabled(True)
            inventory_button.setStyleSheet("background-color: lightblue;")
            npc_button.setEnabled(True)
            npc_button.setStyleSheet("background-color: lightblue;")
            monster_button.setEnabled(True)
            monster_button.setStyleSheet("background-color: lightblue;")
            quest_button.setEnabled(True)
            quest_button.setStyleSheet("background-color: lightblue;")
            manage_attributes_button.setEnabled(True)
            manage_attributes_button.setStyleSheet("background-color: lightblue;")

        inventory_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("Inventory"))
        npc_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("Npc"))
        monster_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("Bestiary"))
        profile_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("Profile"))
        quest_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("Quest"))
        manage_attributes_button.clicked.connect(self.setupManageAttributesMenu)

    def setupManageAttributesMenu(self):
        """
        Set up the manage attributes menu.
        """
        if not self.currentUser.getCharacterSelected():
            QMessageBox.warning(self.main_window, "Error", "Please select a character first!")
            return

        character = self.currentUser.getCharacterSelected()
        available_points = self.character_service.get_attribute_points(character.Id)
        
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
            if attr in ["Strength", "Agility", "Intelligence"]:
                self.buttonList = add_horizontal_buttons(layout, (30, 30), "+")
                increaseBtn = self.buttonList
                increaseBtn.setStyleSheet("background-color: gray;")
                increaseBtn.setEnabled(False)
                # Only add +/- buttons for Strength, Agility, and Intelligence if points are available
                if available_points > 0:
                    increaseBtn.setStyleSheet("background-color: lightblue;")
                    increaseBtn.setEnabled(True)
                    increaseBtn.clicked.connect(lambda checked, a=attr: self.increaseAttribute(a))
                
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
        back_button.clicked.connect(self.setupMainMenu)
        save_button.clicked.connect(lambda: self.saveAttributeChanges(character))

        # Disable save button if no points are available
        if available_points <= 0:
            save_button.setEnabled(False)
            save_button.setStyleSheet("background-color: gray;")
        else:
            save_button.setEnabled(True)
            save_button.setStyleSheet("background-color: lightblue;")

    def increaseAttribute(self, attr):
        """Increase the attribute value if points are available"""
        # Check if we have points available
        current_points = int(self.attributePointsLabel.text().split(": ")[1])
        if current_points > 0:
            self.attributes[attr] += 1
            self.attributeLayouts[attr]["label"].setText(f"{attr}: {self.attributes[attr]}")
            self.attributePointsLabel.setText(f"Attribute Points Available: {current_points - 1}")

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
        SET Strength = %s, 
            Agility = %s, 
            Intelligence = %s,
            AttributePoints = %s
        WHERE ID = %s
        """
        values = (
            self.attributes["Strength"],
            self.attributes["Agility"],
            self.attributes["Intelligence"],
            current_points,  # Update the remaining points
            character.Id
        )
        
        if self.character_service.db_service.execute_query(query, values):
            if self.character_service.db_service.commit():
                # Update the character object with new values
                character.setAttribute("strength", self.attributes["Strength"])
                character.setAttribute("agility", self.attributes["Agility"])
                character.setAttribute("intelligence", self.attributes["Intelligence"])
                QMessageBox.information(self.main_window, "Success", "Character attributes updated successfully!")
                self.setupMainMenu()
            else:
                QMessageBox.warning(self.main_window, "Error", "Failed to save changes!")
        else:
            QMessageBox.warning(self.main_window, "Error", "Failed to update character attributes!") 
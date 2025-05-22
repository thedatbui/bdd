from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

from gui.components.labels import *
from gui.components.butttons import *
from gui.utils import *
from gui.service.player_service import PlayerService

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
        
    
    def setupMainMenu(self):
        """
        Set up the main menu layout.
        """
        clear_screen(self.main_layout)
        self.currentUser = self.main_window.current_user

        self.label = create_title_label(f"Welcome back {self.currentUser.getName()} !")
        self.main_layout.addWidget(self.label)
        
        self.testLayout = add_horizontal_labels(self.main_layout, "ID: ", "Money: ", "Character: ", "Quest: ", "Beast: ")
        self.idLabel = self.testLayout[0]
        self.idLabel.setText(f"ID: {self.currentUser.getId()}")
        self.moneyLabel = self.testLayout[1]
        self.moneyLabel.setText(f"Money: {self.currentUser.getMoney()}")
        self.characterLabel = self.testLayout[2]
        self.characterLabel.setText(f"Character: {self.currentUser.getCharacterSelected().getAttribute('name') if self.currentUser.getCharacterSelected() else 'None'}")
        self.main_layout.addStretch(1)

        self.buttonLayout = add_vertical_buttons(self.main_layout, (200, 50),"Character", "Inventory", "NPC", "Monster", "Profile")
        
        character_button = self.buttonLayout[0]
        inventory_button = self.buttonLayout[1]
        npc_button = self.buttonLayout[2]
        monster_button = self.buttonLayout[3]
        profile_button = self.buttonLayout[4]

        self.main_layout.addStretch(1)
        #Connect each button to its appropriate function
        character_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("Character"))
        if self.currentUser.getCharacterSelected() is None:
            inventory_button.setEnabled(False)
            inventory_button.setStyleSheet("background-color: gray;")
            npc_button.setEnabled(False)
            npc_button.setStyleSheet("background-color: gray;")
        else:
            inventory_button.setEnabled(True)
            inventory_button.setStyleSheet("background-color: lightblue;")
            npc_button.setEnabled(True)
            npc_button.setStyleSheet("background-color: lightblue;")
        inventory_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("Inventory"))
        npc_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("Npc"))
        # monster_button.clicked.connect(self.setupMonsterMenu)
        profile_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("Profile"))   
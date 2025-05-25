from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QMessageBox
from PyQt5.QtCore import Qt
import re

from gui.components.labels import *
from gui.components.inputs import *
from gui.components.butttons import *
from gui.service.player_service import *
from gui.service.db_service import *
from gui.service.npc_service import *
from gui.service.Bestiary_service import BestiaryService
from gui.service.character_service import CharacterService
from gui.utils import *
from gui.models.Npc import *
from gui.models.Object import *

class QuestScreen:
    """The Quest screen of the application."""
    
    def __init__(self, main_window, scene_manager):
        """
        Initialize the Quest screen.
        
        Args:
            main_window: The application's main window
            scene_manager: The scene manager to handle screen transitions
        """
        self.main_window = main_window
        self.scene_manager = scene_manager
        self.main_layout = main_window.mainLayout
        self.player_service = PlayerService()
        self.npc_service = NpcService()
        self.db = DatabaseService()
        self.bestiary_service = BestiaryService()
        self.character_service = CharacterService()
    
    
    def setupQuestMenu(self):
        """Set up the Quest menu."""
        clear_screen(self.main_layout)
        self.currentUser = self.main_window.current_user
        self.character = self.currentUser.getCharacterSelected()
        self.characterId = self.character.getAttribute("Id")
        self.label = create_title_label("Quest Menu")
        self.main_layout.addWidget(self.label)

        self.quest_label = create_label(f"Quests in progress:{self.character_service.get_selected_quest(self.characterId)}")
        self.main_layout.addWidget(self.quest_label)

        self.quests = self.character_service.get_quest_list(self.characterId)

        self.layout = QHBoxLayout()
        self.questList = QtWidgets.QListWidget()

        for quest in self.quests:
            item = QtWidgets.QListWidgetItem(quest)
            self.questList.addItem(item)
        
        self.questList.currentItemChanged.connect(self.displayQuestDetails)
        self.questList.doubleClicked.connect(self.selectQuest)
        self.layout.addWidget(self.questList)

        self.questDetails = QLabel("Select a quest to see details.")
        self.questDetails.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.layout.addWidget(self.questDetails)

        self.main_layout.addLayout(self.layout)

        self.backButtonList = add_horizontal_buttons(self.main_layout, (200, 50), "Back")
        self.backButton = self.backButtonList
        self.backButton.clicked.connect(lambda:  self.scene_manager.switch_to_menu("Main Menu"))

    def displayQuestDetails(self, current, previous):
        """Display the details of the selected quest."""
        if current:
            quest_name = current.text()
            quest_details = self.npc_service.get_quest_details(quest_name)
            if quest_details:
                self.questDetails.setText(f"Quest: {quest_name}\n Details: {quest_details.get_name()} \n Description: {quest_details.get_description()}")
            else:
                self.questDetails.setText("No details available for this quest.")
        else:
            self.questDetails.setText("Select a quest to see details.")


    def selectQuest(self):
        self.character_service.select_quest(self.characterId, self.questList.currentItem().text())
        QMessageBox.information(self.main_window, "Quest Selected", f"You have selected the quest: {self.questList.currentItem().text()}")
        self.quest_label.setText(f"Quests in progress: {self.character_service.get_selected_quest(self.characterId)}")


      
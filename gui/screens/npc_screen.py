from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QMessageBox
from PyQt5.QtCore import Qt
import re

from gui.components.labels import create_title_label, create_label
from gui.components.inputs import add_labeled_input
from gui.service.player_service import *
from gui.service.db_service import *
from gui.service.npc_service import *
from gui.service.Bestiary_service import BestiaryService
from gui.service.character_service import CharacterService
from gui.utils import *
from gui.models.Npc import *
from gui.models.Object import *


class NpcScreen:
    """The NPC screen of the application."""
    
    def __init__(self, main_window, scene_manager):
        """
        Initialize the NPC screen.
        
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
    
    def setupNpcMenu(self):
        """
        Set up the NPC menu.
        """
        clear_screen(self.main_layout)

        self.currentUser = self.main_window.current_user
        self.character = self.currentUser.getCharacterSelected()
        self.label = create_title_label("NPC Menu")
        self.main_layout.addWidget(self.label)

        self.label = create_label("Who would you like to talk to?")
        self.main_layout.addWidget(self.label)
        
        self.npcLayout = QtWidgets.QListWidget()
        self.main_layout.addWidget(self.npcLayout)

        self.npcList = self.npc_service.get_npc()
        for npc in self.npcList:
            item = QtWidgets.QListWidgetItem(npc.getName())
            self.npcLayout.addItem(item)

        self.npcLayout.doubleClicked.connect(self.on_npc_selected)
        self.buttonList = setupButtons(self.main_layout, (200,50), "Back")
        back_button = self.buttonList
        back_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("Main Menu"))
    
    def on_npc_selected(self, item):
        """
        Select the NPC when double-clicked.
        """
        current_row = self.npcLayout.currentRow()
        if current_row >= 0:
            self.npc = self.npcList[current_row]
            # Update character name in main menu
            
            self.shopAndQuest(self.npc.getDialogue(), self.npc.getId())
    
    def shopAndQuest(self, dialogue, Id):
        """
        Set up the shop and quest menu.
        """
        clear_screen(self.main_layout)
      
        self.label = create_title_label(f"{dialogue}", 12)
        self.main_layout.addWidget(self.label)

        self.label = create_label(f"Money: {self.currentUser.getMoney()}")
        self.main_layout.addWidget(self.label)

        self.subLayout = QHBoxLayout()
        self.subItemLayout = QVBoxLayout()
        self.label = QLabel("Shop")
        self.itemList = QtWidgets.QListWidget()
        
        ItemResult = self.npc_service.get_item_details(Id)
        for items in ItemResult:
            self.itemList.addItem(items)
        # for row in ItemResult:
        #     item = QtWidgets.QListWidgetItem(f"{row[0]} - {row[1]} gold - {row[2]} available")
        #     self.itemList.addItem(item)
                
        self.itemList.doubleClicked.connect(self.on_itemSelected)
        self.subItemLayout.addWidget(self.label)
        self.subItemLayout.addWidget(self.itemList)
        self.subQuestLayout = QVBoxLayout()

        self.label = QLabel("Quest")
        self.questList = QtWidgets.QListWidget()
        self.quest = self.npc_service.get_quest_npc(Id)
        for quest in self.quest:
            if self.npc_service.check_existing_quest(quest):
                item = QtWidgets.QListWidgetItem(quest)
                self.questList.addItem(item)

        self.questList.currentItemChanged.connect(self.on_quest_selected)
        self.questList.doubleClicked.connect(self.confirm_quest_selection)
        self.subQuestLayout.addWidget(self.label)
        self.subQuestLayout.addWidget(self.questList)
        self.subLayout.addLayout(self.subItemLayout)
        self.subLayout.addLayout(self.subQuestLayout)
        self.main_layout.addLayout(self.subLayout)

        self.label = create_label("Quest Details", 10)
        self.main_layout.addWidget(self.label)

        self.buttonList = setupButtons(self.main_layout, (200,50), "Back")
        back_button = self.buttonList
        back_button.clicked.connect(self.setupNpcMenu)
       
    def on_itemSelected(self, item):
        """
        Select the item when double-clicked.
        """

        current_row = self.itemList.currentRow()
        if current_row >= 0:
            item = self.itemList.item(current_row).text()
            item_name, item_price, item_quantity = item.split(" - ")
            item_price = int(item_price.split(" ")[0])
            item_quantity = int(item_quantity.split(" ")[0])
            
            # check if the current player has enough space in the inventory
            query = "SELECT COUNT(*) FROM Inventory WHERE characterID = %s"
            self.db.execute_query(query, (self.character.getAttribute("Id"),))
            inventory_count = self.db.fetch_one()[0]

            if inventory_count < self.currentUser.getInventorySlot():
                if item_quantity > 0 :
                    query = "SELECT * FROM ObjectTest WHERE ObjectName = %s"
                    self.db.execute_query(query, (item_name,))
                    result = self.db.fetch_one()
                    self.object = Object(result[1], result[2], result[3], result[4], result[5], result[6])
                    self.currentUser.addItemToInventory(self.object)

                    query = "UPDATE NPCInventory SET Quantity = Quantity - 1 WHERE ObjectName = %s AND NPCID = %s"
                    self.db.execute_query(query, (item_name, self.npc.getId()))
                    self.db.commit()
                    item_quantity -= 1
                    self.itemList.item(current_row).setText(f"{item_name} - {item_price} gold - {item_quantity} available")

                    # update Inventory

                else:
                    QMessageBox.warning(
                        self.main_window,
                        "Out of Stock",
                        f"'{item_name}' is out of stock."
                    )
            else:
                QMessageBox.warning(
                    self.main_window,
                    "Inventory Full",
                    f"Your inventory is full. Please remove an item before purchasing."
                )

            # if self.currentUser.getMoney() >= item_price:
            #     # Update NPC inventory
            #     query = "UPDATE NPCInventory SET Quantity = Quantity - 1 WHERE ObjectName = %s AND NPCID = %s"
            #     self.cursor.execute(query, (item_name, self.npc.getId()))
            #     self.connection.commit()
                
            #     QMessageBox.information(
            #         self.main_window,
            #         "Success",
            #         f"You have purchased '{item_name}' for {item_price} gold."
            #     )
            # else:
            #     QMessageBox.warning(
            #         self.main_window,
            #         "Insufficient Funds",
            #         f"You do not have enough money to purchase '{item_name}'."
            #     )

    def on_quest_selected(self, item):
        """
        Handle quest selection.
        """
        current_row = self.questList.currentRow()
        if current_row >= 0:
            quest_name = self.questList.currentItem().text()
            
            try:
                self.db.fetch_all()
            except:
                pass
            
            query = "SELECT * FROM Quest WHERE QuestName = %s"
            if self.db.execute_query(query, (quest_name,)):
                result = self.db.fetch_one()
                print(result)
                
                if result:
                    quest_obj = Quest(result[0], result[1], result[2], result[3], result[4])
                    self.label.setText(
                        f"Quest Name: {quest_obj.get_name()}\n"
                        f"Description: {quest_obj.get_description()}\n"
                        f"Difficulty: {quest_obj.get_difficulty()}\n"
                        f"Reward: {quest_obj.get_reward()} gold"
                    )
                    self.quest_details = quest_obj
                else:
                    self.label.setText(f"No details found for quest: {quest_name}")

    def confirm_quest_selection(self):
        """
        Confirm the quest selection.
        """
        possible_kill_keys = ["tuez", "tuer", "éliminer", "éliminez"]
        current_row = self.questList.currentRow()
        if current_row >= 0:
            quest_name = self.questList.currentItem().text()
            # self.currentUser.setQuestSelected(quest_name)
            QMessageBox.information(
                self.main_window,
                "Quest Accepted",
                f"You have accepted the quest: {quest_name}."
            )
            for key in possible_kill_keys:
                if key in self.quest_details.get_description().lower():
                    for bestiary in self.bestiary_service.get_bestiaryName():
                        if bestiary.lower() in self.quest_details.get_description().lower():
                            match = re.search(r'\b\d+\b', self.quest_details.get_description())
                            if match:
                                if not self.character_service.insert_character_killQuest(
                                    self.character.getAttribute("Id"),
                                    quest_name,
                                    bestiary,
                                    int(match.group())
                                ):
                                    QMessageBox.warning(
                                        self.main_window,
                                        "Quest Error",
                                        "Quest already exists or could not be added."
                                    )
                                    return
                                self.character_service.select_quest(
                                    self.character.getAttribute("Id"),
                                    quest_name
                                )
                            self.scene_manager.switch_to_menu("Main Menu")
                            return
            
            

            
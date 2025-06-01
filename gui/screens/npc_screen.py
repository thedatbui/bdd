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
from gui.service.inventory_service import InventoryService
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
        self.inventory_service = InventoryService()

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

        self.currentUser  = self.main_window.current_user
        self.character    = self.currentUser.getCharacterSelected()
        self.characterId  = self.character.getAttribute("Id")
      
        self.label = create_title_label(f"{dialogue}", 12)
        self.main_layout.addWidget(self.label)

        gold = self.player_service.get_wallet_for_character(self.characterId)
        self.goldLabel = create_label(f"Gold: {gold}")

        self.main_layout.addWidget(self.goldLabel)

        self.subLayout = QHBoxLayout()
        self.subItemLayout = QVBoxLayout()
        self.label = QLabel("Shop")
        self.itemList = QtWidgets.QListWidget()
        
        ItemResult = self.npc_service.get_item_details(Id)
        for items in ItemResult:
            self.itemList.addItem(items)
                
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
            item_name, item_price_text, item_quantity_text = item.split(" - ")
            item_price = int(item_price_text.split(" ")[0])
            item_quantity = int(item_quantity_text.split(" ")[0])
            
            # Check if item is in stock
            if item_quantity <= 0:
                QMessageBox.warning(
                    self.main_window,
                    "Out of Stock",
                    f"'{item_name}' is out of stock."
                )
                return
                
            # Check if the player has enough money
            if self.currentUser.getMoney() < item_price:
                QMessageBox.warning(
                    self.main_window,
                    "Insufficient Funds",
                    f"You do not have enough money to purchase '{item_name}'."
                )
                return
                
            # Check if the player's inventory is full
            inventory_count = self.inventory_service.get_item_quantities(self.character.getAttribute("Id"))
            print(f"Current inventory count: {inventory_count}")
            if inventory_count >= self.currentUser.getInventorySlot():
                QMessageBox.warning(
                    self.main_window,
                    "Inventory Full",
                    f"Your inventory is full. Please remove an item before purchasing."
                )
                return
            try:
                # 1. Update NPC inventory (reduce quantity)
                self.npc_service.update_npc_inventory(
                    self.npc.getId(),
                    item_name
                )
                
                # 2. Update player wallet
                new_balance = self.currentUser.getMoney() - item_price
                self.player_service.update_player_wallet(
                    self.currentUser.getId(),
                    new_balance
                )
                    
                # 3. Create the object and add to player inventory
                self.currentUser.addItemToInventory(item_name)
                
                # Transaction successful, update UI and notify user
                self.currentUser.setMoney(new_balance)
                self.goldLabel.setText(f"Gold: {new_balance}")
                
                # Update the list item to show the new quantity
                self.itemList.item(current_row).setText(f"{item_name} - {item_price} gold - {item_quantity - 1} available")
                
                QMessageBox.information(
                    self.main_window,
                    "Success",
                    f"You have purchased '{item_name}' for {item_price} gold."
                )
                self.db.commit()
            except Exception as e:
                # Handle any errors that occurred during the transaction
                print(f"Error during purchase: {e}")
                QMessageBox.critical(
                    self.main_window,
                    "Transaction Error",
                    f"An error occurred during the purchase: {str(e)}"
                )

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
            
            self.quest_obj = self.npc_service.get_quest_details(quest_name)
            if not self.quest_obj:
                QMessageBox.warning(
                    self.main_window,
                    "Quest Error",
                    f"Quest '{quest_name}' not found."
                )
                return
            questGold = self.npc_service.get_gold_quest(self.quest_obj.get_id())
            self.label.setText(
                f"Quest Name: {self.quest_obj.get_name()}\n"
                f"Description: {self.quest_obj.get_description()}\n"
                f"Difficulty: {self.quest_obj.get_difficulty()}\n"
                f"Xp rewards: {self.quest_obj.get_reward()} Xp \n"
                f"Gold rewards: {questGold} Gold\n"
                )
         
            self.db.commit()

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
                if key in self.quest_obj.get_description().lower():
                    for bestiary in self.bestiary_service.get_bestiaryName():
                        if bestiary.lower() in self.quest_obj.get_description().lower():
                            match = re.search(r'\b\d+\b', self.quest_obj.get_description())
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
                          
            
            

            
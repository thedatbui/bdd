from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QMessageBox
from PyQt5.QtCore import Qt

from gui.components.labels import create_title_label, create_label
from gui.components.inputs import add_labeled_input
from gui.service.player_service import *
from gui.service.db_service import *
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
        self.db = DatabaseService()
    
    def setupNpcMenu(self):
        """
        Set up the NPC menu.
        """
        clear_screen(self.main_layout)

        self.currentUser = self.main_window.current_user
        self.label = QLabel(f"NPC Menu")
        self.label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.label.setFont(QtGui.QFont("Arial", 15))
        self.label.setStyleSheet("color: blue;")
        self.main_layout.addWidget(self.label)

        self.label = QLabel(f"Who would you like to talk to?")
        self.label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.label.setFont(QtGui.QFont("Arial", 15))
        self.label.setStyleSheet("color: blue;")
        self.main_layout.addWidget(self.label)
        
        self.npcLayout = QtWidgets.QListWidget()
        self.main_layout.addWidget(self.npcLayout)

        self.npcList = []
        self.db.execute_query("SELECT * FROM NPC;")
        result = self.db.fetch_all()
        if result:
            for row in result:
                item = QtWidgets.QListWidgetItem(row[1])
                self.npcList.append(Npc(row[0], row[1], row[2], row[3]))
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
      
        self.label = QLabel(f"{dialogue}")
        self.label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.label.setFont(QtGui.QFont("Arial", 15))
        self.label.setStyleSheet("color: blue;")
        self.main_layout.addWidget(self.label)

        self.label = QLabel(f"Money: {self.currentUser.getMoney()}")
        self.label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.label.setFont(QtGui.QFont("Arial", 15))
        self.label.setStyleSheet("color: blue;")
        self.main_layout.addWidget(self.label)

        self.subLayout = QHBoxLayout()
        self.subItemLayout = QVBoxLayout()
        self.label = QLabel("Shop")
        self.itemList = QtWidgets.QListWidget()
        
        query = "SELECT ObjectTest.ObjectName, ObjectTest.price, NPCInventory.Quantity FROM ObjectTest, NPCInventory " \
        "WHERE NPCInventory.ObjectName = ObjectTest.ObjectName AND NPCInventory.NPCID = %s;"
        self.db.execute_query(query, (Id,))
        ItemResult = self.db.fetch_all()
        if ItemResult:
            for row in ItemResult:
                item = QtWidgets.QListWidgetItem(f"{row[0]} - {row[1]} gold - {row[2]} available")
                self.itemList.addItem(item)
        self.itemList.doubleClicked.connect(self.on_itemSelected)
        self.subItemLayout.addWidget(self.label)
        self.subItemLayout.addWidget(self.itemList)
        self.subQuestLayout = QVBoxLayout()
        self.label = QLabel("Quest")
        self.questList = QtWidgets.QListWidget()
        self.subQuestLayout.addWidget(self.label)
        self.subQuestLayout.addWidget(self.questList)
        self.subLayout.addLayout(self.subItemLayout)
        self.subLayout.addLayout(self.subQuestLayout)
        self.main_layout.addLayout(self.subLayout)

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
            query = "SELECT COUNT(*) FROM Inventory WHERE PlayerID = %s"
            self.db.execute_query(query, (self.currentUser.getId(),))
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
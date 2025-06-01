from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QMessageBox
from PyQt5.QtCore import Qt

from gui.components.labels import *
from gui.components.butttons import *
from gui.service.player_service import PlayerService
from gui.service.db_service import DatabaseService
from gui.service.inventory_service import InventoryService
from gui.utils import *


class InventoryMenuScreen:
    """
    The inventory menu screen of the application.
    This class sets up the inventory menu screen and its components.
    """

    def __init__(self, main_window, scene_manager):
        """
        Initialize the inventory menu screen.

        Args:
            main_window: The application's main window
            scene_manager: The scene manager to handle screen transitions
        """
        self.main_window = main_window
        self.scene_manager = scene_manager
        self.main_layout = main_window.mainLayout
        self.player_service = PlayerService()
        self.db = DatabaseService()
        self.inventory_service = InventoryService()
    
    def setupInventoryMenu(self):
        """
        Set up the inventory menu.
        """
        clear_screen(self.main_layout)
            
        self.currentUser = self.main_window.current_user
        self.character = self.currentUser.getCharacterSelected()
        self.label = create_title_label("Inventory Menu")
        self.main_layout.addWidget(self.label)
        
        self.label = add_horizontal_labels(self.main_layout, "Current Weight: 0", "Max Weight: 0")
        self.currentWeightLabel = self.label[0]
        self.maxWeightLabel = self.label[1]
        self.currentWeight = self.inventory_service.get_item_quantities(self.character.getAttribute("Id"))
        self.db.execute_query(
            "SELECT InventorySlot FROM Player WHERE ID = %s",
            (self.currentUser.getId(),)
        )
        max_slots = self.db.fetch_one()[0]
        self.currentWeightLabel.setText(f"Current Weight: {self.currentWeight}")
        self.maxWeightLabel.setText(f"Max Weight: {max_slots}")

        self.subLayout = QHBoxLayout()
        self.itemList = QtWidgets.QListWidget()
        result = self.inventory_service.get_inventory_items(self.character.getAttribute("Id"))

        for row in result:
            item = QtWidgets.QListWidgetItem(row)
            self.itemList.addItem(item)

        self.itemList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.itemList.customContextMenuRequested.connect(self.show_context_menu)
        self.subLayout.addWidget(self.itemList)
        self.itemList.currentItemChanged.connect(self.on_itemChanged)

        self.label = create_label("Object Details", 10, "blue", Qt.AlignTop | Qt.AlignLeft)
  
        self.subLayout.addWidget(self.label)
        self.main_layout.addLayout(self.subLayout)

        self.buttonList = add_horizontal_buttons(self.main_layout, (200, 50), "Back")
        back_button = self.buttonList
        back_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("Main Menu"))

    def on_itemChanged(self, current, previous):
        """
        Update the item details when an item is selected in the list.
        """
        if current:
            item_name = self.itemList.currentItem().text()
            result = self.inventory_service.get_item_details(item_name)
            current_count = self.inventory_service.get_item_quantity(self.character.getAttribute("Id"), item_name)
            self.object_details = f"""Object Details:
            Name: {result.getName()}
            Type: {result.getType()}
            Strength: {result.getStrength()}
            Defence: {result.getDefence()}
            Effects: {result.getEffects()}
            Price: {result.getPrice()}
            Quantity: {current_count}
            """
            self.label.setText(self.object_details)
    
    def update_item_details(self, item_name):
        """
        Update the item details when an item is selected in the list.
        """
        result = self.inventory_service.get_item_details(item_name)
        current_count = self.inventory_service.get_item_quantity(self.character.getAttribute("Id"), item_name)
        self.object_details = f"""Object Details:
        Name: {result.getName()}
        Type: {result.getType()}
        Strength: {result.getStrength()}
        Defence: {result.getDefence()}
        Effects: {result.getEffects()}
        Price: {result.getPrice()}
        Quantity: {current_count}
        """
        self.label.setText(self.object_details)

    def show_context_menu(self, position):
        """
        Show the context menu when right-clicking on an item in the list.
        """
        context_menu = QtWidgets.QMenu(self.itemList)
        delete_action = context_menu.addAction("Delete")
        action = context_menu.exec_(self.itemList.viewport().mapToGlobal(position))
        
        if action == delete_action:
            self.delete_item()
    
    def delete_item(self):
        """
        Delete the selected item from the inventory.
        """
        current_row = self.itemList.currentRow()
        item_name = self.itemList.item(current_row).text()
        current_count = self.inventory_service.get_item_quantity(self.character.getAttribute("Id"), self.itemList.item(current_row).text())
        self.currentWeight -= 1
        if current_row >= 0:
            if current_count > 1:
                print("Deleting item")
                self.inventory_service.update_quantity(self.character.getAttribute("Id"), item_name, current_count - 1)
                self.update_item_details(item_name)
            else:
                self.inventory_service.delete_item(self.currentUser.getId(), item_name)
                self.itemList.takeItem(current_row)
                QMessageBox.information(self.main_window, "Success", f"{item_name} has been deleted from your inventory.")
        self.currentWeightLabel.setText(f"Current Weight: {self.currentWeight}")
        self.label.setText("Object Details: ")
        self.db.commit()
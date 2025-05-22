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
            object_details = f"""Object Details:
            Name: {result.getName()}
            Type: {result.getType()}
            Strength: {result.getStrength()}
            Defence: {result.getDefence()}
            Effects: {result.getEffects()}
            Price: {result.getPrice()}"""
            self.label.setText(object_details)
    
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
        if current_row >= 0:
            item_name = self.itemList.item(current_row).text()
            self.inventory_service.delete_item(self.currentUser.getId(), item_name)
            self.itemList.takeItem(current_row)
            QMessageBox.information(self.main_window, "Success", f"{item_name} has been deleted from your inventory.")
            self.db.commit()
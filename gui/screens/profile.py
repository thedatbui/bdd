from PyQt5.QtWidgets import QVBoxLayout, QWidget, QInputDialog
from PyQt5.QtCore import Qt

from gui.components.labels import *
from gui.components.butttons import *
from gui.utils import *
from gui.service.player_service import PlayerService

class ProfileScreen:
    def __init__(self, main_window, scene_manager):
        """
        Initialize the profile screen.
        
        Args:
            main_window: The application's main window
            scene_manager: The scene manager to handle screen transitions
        """
        self.main_window = main_window
        self.scene_manager = scene_manager
        self.main_layout = main_window.mainLayout
        self.player_service = PlayerService()

    def setupProfileMenu(self):
        """
        Set up the profile menu layout.
        """
        clear_screen(self.main_layout)
        self.currentUser = self.main_window.current_user

        self.label = create_title_label(f"Profile")
        self.main_layout.addWidget(self.label)

        self.testLayout = add_vertical_labels(self.main_layout, "name: ", "ID: ", "Money: ", "Character: ", "Quest: ", "Beast: ")
        self.nameLabel = self.testLayout[0]
        self.nameLabel.setText(f"Name: {self.currentUser.getName()}")
        self.idLabel = self.testLayout[1]
        self.idLabel.setText(f"ID: {self.currentUser.getId()}")
        self.moneyLabel = self.testLayout[2]
        self.moneyLabel.setText(f"Money: {self.currentUser.getMoney()}")
        self.characterLabel = self.testLayout[3]
        self.characterLabel.setText(f"Character: {self.currentUser.getCharacterSelected().name}")
        self.main_layout.addStretch(1)

        # Add buttons for profile actions
        self.buttonLayout = add_vertical_buttons(self.main_layout, (200, 50), "Change userName", "Log out", "Delete Account", "Back")
        
        edit_username_button = self.buttonLayout[0]
        logout_button = self.buttonLayout[1]
        delete_account_button = self.buttonLayout[2]
        back_button = self.buttonLayout[3]

        edit_username_button.clicked.connect(self.editUsername)
        logout_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("IntroMenu"))
        delete_account_button.clicked.connect(self.deleteAccount)
        back_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("Main Menu"))

    def deleteAccount(self):
        """
        Delete the current user's account.
        """
        confirm = QMessageBox.question(
            self.main_window,
            "Confirm Deletion",
            f"Are you sure you want to delete account '{self.currentUser.getName()}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                self.player_service.delete_player(self.currentUser)
                QMessageBox.information(
                    self.main_window,
                    "Success",
                    f"Account '{self.currentUser.getName()}' has been deleted."
                )

                 # Clear user data
                self.main_window.current_user = None

                # Switch to start menu
                self.scene_manager.switch_to_menu("IntroMenu")
            except Exception as e:
                QMessageBox.critical(
                    self.main_window,
                    "Error",
                    f"Failed to delete account: {str(e)}"
                )
    
    def editUsername(self):
        """
        Edit the current user's username.
        """
        new_username, ok = QInputDialog.getText(self.main_window, "Edit Username", "Enter new username:")
        
        if ok and new_username:
            try:
                self.player_service.update_player_username(self.currentUser, new_username)
                QMessageBox.information(
                    self.main_window,
                    "Success",
                    f"Username updated to '{new_username}'."
                )
                
                # Update the label
                self.nameLabel.setText(f"Name: {new_username}")
            except Exception as e:
                QMessageBox.critical(
                    self.main_window,
                    "Error",
                    f"Failed to update username: {str(e)}"
                )
        
            
from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QMessageBox
from PyQt5.QtCore import Qt

from gui.components.labels import create_title_label, create_label
from gui.components.inputs import add_labeled_input
from gui.service.player_service import PlayerService
from gui.service.db_service import DatabaseService
from gui.models.Player import Player
from gui.components.inputs import *
from gui.utils import *

class LoginScreen:
    """The login screen of the application."""
    
    def __init__(self, main_window, scene_manager):
        """
        Initialize the login screen.
        
        Args:
            main_window: The application's main window
            scene_manager: The scene manager to handle screen transitions
        """
        self.main_window = main_window
        self.scene_manager = scene_manager
        self.main_layout = main_window.mainLayout
        self.player_service = PlayerService()
        self.db = DatabaseService()
        
    
    def setup(self):
        """Set up the login screen UI."""
        # Clear the current layout
        clear_screen(self.main_layout)
        
        # Create title label
        self.title_label = create_title_label(
            "Welcome to the RPG Game!",
            font_size=20,
            color="blue",
            alignment=Qt.AlignTop | Qt.AlignCenter
        )
        self.main_layout.addWidget(self.title_label)
        
        # Create message label
        self.message_label = create_label(
            "",
            font_size=14,
            color="red",
            alignment=Qt.AlignCenter
        )
        self.main_layout.addWidget(self.message_label)
        
        # Create input field
        self.input_field = add_labeled_input(
            self.main_layout,
            "Enter your username:"
        )
        self.input_field.returnPressed.connect(self.on_input_submitted)
    
    def on_input_submitted(self):
        """Handle username submission."""
        username = self.input_field.text()
        
        if not username:
            self.message_label.setText("Please enter a username.")
            return
        
        player = self.player_service.get_player_by_username(username)
        
        if player:
            self.main_window.current_user = player
            self.scene_manager.switch_to_menu("Main Menu")
        else:
            QMessageBox.warning(
                self.main_window,
                "Login Error",
                f"Username {username} does not exist."
            )
            self.input_field.clear()
            self.input_field.setFocus()
    
    
    def setupCreateAccountMenu(self):
        """
        Set up the create account menu.
        """
        clear_screen(self.main_layout)

        self.titleLabel = create_title_label("Create Account")
        self.main_layout.addWidget(self.titleLabel)

        self.inputField = create_line_edit("Enter your character name")
        self.main_layout.addWidget(self.inputField)

        self.main_layout.addStretch(1)
        self.messageLabel = setupLabel(self.main_layout, "")
        self.messageLabel.setAlignment(Qt.AlignCenter)
        self.messageLabel.setFont(QtGui.QFont("Arial", 14))
        self.main_layout.addStretch(1)

        self.buttonList  = setupButtons(self.main_layout, (200,50), "Create Account", "Back")
        create_account_button = self.buttonList[0]
        back_button = self.buttonList[1]
        # Connect each button to its appropriate function
        create_account_button.clicked.connect(self.createAccount)
        back_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("IntroMenu"))

    def createAccount(self):
        """Handle account creation"""
        userName = self.inputField.text()

        if not userName:
           QMessageBox.warning(self.main_window, "Input Error", "Please enter a username.")
           
        if userName:
            #check if the username already exists
            query = "SELECT * FROM Player WHERE UserName = %s"
            self.db.execute_query(query, (userName,))
            result = self.db.fetch_one()
            if result:
                QMessageBox.warning(self.main_window, "Input Error", f"Username {userName} already exists.")
                self.inputField.clear()
                self.inputField.setFocus()
                return
            
            # Create a new Player object
            self.currentUser = Player(userName, None, None, None, None)
            # Insert the new player into the database
            query = "INSERT INTO Player (UserName) VALUES (%s)"
            self.db.execute_query(query, (userName,))
            self.db.commit()

            response = QMessageBox.information(self.main_window, "Success", f"Account {userName} created successfully.")
            if response == QMessageBox.Ok:
                self.scene_manager.switch_to_menu("IntroMenu")
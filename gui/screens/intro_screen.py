from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

from gui.components.labels import create_title_label
from gui.components.butttons import add_horizontal_buttons
from gui.utils import *

class IntroScreen:
    """The initial welcome screen of the application."""
    
    def __init__(self, main_window, scene_manager):
        """
        Initialize the intro screen.
        
        Args:
            main_window: The application's main window
            scene_manager: The scene manager to handle screen transitions
        """
        self.main_window = main_window
        self.scene_manager = scene_manager
        self.main_layout = main_window.mainLayout
    
    def setup(self):
        """Set up the intro screen UI."""
        # Clear the current layout
        clear_screen(self.main_layout)
        
        # Create title label
        title = create_title_label(
            "Welcome to the RPG Game!",
            font_size=20,
            color="blue",
            alignment=Qt.AlignTop | Qt.AlignCenter
        )
        self.main_layout.addWidget(title)
        
        # Create buttons
        self.button_list = add_horizontal_buttons(
            self.main_layout,
            (200, 50),
            "Log In",
            "Create Account"
        )
        
        # Connect button events
        login_button = self.button_list[0]
        create_account_button = self.button_list[1]
        
        login_button.clicked.connect(
            lambda: self.scene_manager.switch_to_menu("LogIn")
        )
        create_account_button.clicked.connect(
            lambda: self.scene_manager.switch_to_menu("Create Account")
        )
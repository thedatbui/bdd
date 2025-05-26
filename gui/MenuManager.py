from gui.utils import *
from gui.screens.intro_screen import IntroScreen
from gui.screens.login_screen import LoginScreen
from gui.screens.main_menu_screen import MainMenuScreen
from gui.screens.character_screen import CharacterMenuScreen
from gui.screens.inventory_screen import InventoryMenuScreen
from gui.screens.npc_screen import NpcScreen
from gui.screens.profile import ProfileScreen
from gui.screens.bestiary_screen import BestiaryScreen
class SceneManager:
    """Manager for switching between different screens."""
    
    def __init__(self, main_window):
        """
        Initialize the scene manager.
        
        Args:
            main_window: The application's main window
        """
        self.main_window = main_window
        
        self.intro_screen = IntroScreen(main_window, self)
        self.login_screen = LoginScreen(main_window, self)
        self.mainMenu_screen = MainMenuScreen(main_window, self)
        self.character_screen = CharacterMenuScreen(main_window, self)
        self.inventory_screen = InventoryMenuScreen(main_window, self)
        self.npc_screen = NpcScreen(main_window, self)
        self.profile_screen = ProfileScreen(main_window, self)
        self.bestiary_screen = BestiaryScreen(main_window, self)
    
    def set_scene(self):
        """Set the current scene based on the current menu state."""
        current_state = getMenuState()
        
        if current_state == 0:
            self.intro_screen.setup()
        elif current_state == 1:
            self.login_screen.setup()
        elif current_state == 2:
            self.login_screen.setupCreateAccountMenu()
        elif current_state == 3:
            self.mainMenu_screen.setupMainMenu()
        elif current_state == 4:
            self.character_screen.setupCharacterMenu()
        elif current_state == 5:
            self.inventory_screen.setupInventoryMenu()
        elif current_state == 6:
            self.npc_screen.setupNpcMenu()
        elif current_state == 7:
             self.bestiary_screen.setupBestiaryMenu()
        elif current_state == 8:
            self.profile_screen.setupProfileMenu()
    
    def switch_to_menu(self, menu_state):
        """
        Switch to a different menu.
        
        Args:
            menu_state: The menu state to switch to
        """
        setMenuState(menu_state)
        self.set_scene()
        
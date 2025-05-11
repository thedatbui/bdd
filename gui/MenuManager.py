from gui.SetupMenu import SetupMenu
from gui.utils import *

class SceneManager:
    """
    SceneManager class to manage different scenes in the game.
    """
    def __init__(self, main_window):
        # We'll import SetupMenu here to avoid circular imports
        self.main_window = main_window
        self.setup_menu = SetupMenu(main_window)
        self.setup_menu.scene_manager = self

    def set_scene(self):
        """
        Set the current scene based on the scene name.
        """
        current_state = getMenuState()
        
        if current_state == 0:
            print("Setting up Start Menu")
            self.setup_menu.setupStartMenu()
        elif current_state == 1:
            print("Setting up Login Menu")
            self.setup_menu.setupLogInMenu()
        elif current_state == 2:
            self.setup_menu.setupCreateAccountMenu()
        elif current_state == 3:
            self.setup_menu.setupMainMenu()
        elif current_state == 4:
            self.setup_menu.setupCharacterMenu()
            
        # elif currentMenuState == 5:
        #     self.current_scene = InventoryScene(self.main_window)
        # elif currentMenuState == 6:
        #     self.current_scene = QuestScene(self.main_window)
        # elif currentMenuState == 7:
        #     self.current_scene = NpcScene(self.main_window)
        # elif currentMenuState == 8:
        #     self.current_scene = BestiaryScene(self.main_window)
        # elif currentMenuState == 9:
        #     self.current_scene = ExitScene(self.main_window)
    
    def switch_to_menu(self, menu_name):
        """
        Switch to a different menu by name and refresh the UI.
        """
        setMenuState(menu_name)
        self.set_scene()
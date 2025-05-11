from gui.utils import *
from gui.Player import Player
from src.db_utils.connectToDataBase import *
from gui.Character import Character

class SetupMenu:
    """
    SetupMenu class to manage the setup menu of the game.
    """
    def __init__(self, main_window):
        self.main_window = main_window
        self.mainLayout = self.main_window.mainLayout
        self.connection = get_connection()
        self.cursor = get_cursor()
        self.currentUser = Player(None, None)

    def setupStartMenu(self):
        """
        Set up the main menu layout.
        """
        clear_screen(self.mainLayout)

        # Create title label
        title = QLabel("Welcome to the RPG Game!")
        title.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        title.setFont(QtGui.QFont("Arial", 20))
        title.setStyleSheet("color: blue;")
        self.mainLayout.addWidget(title)
        
        # Create buttons
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
        
        self.buttonList = setupButtons(self.mainLayout, (200,50), "Log In", "Create Account")
        login_button = self.buttonList[0]
        create_account_button = self.buttonList[1]
        # Connect buttons to scene manager
        login_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("LogIn"))
        create_account_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("Create Account"))
        

    def setupLogInMenu(self):
        """
        Set up the main window and its components.
        """
        clear_screen(self.mainLayout)
        self.login = True

        self.titleLabel = setupLabel(self.mainLayout,  "Welcome to the RPG Game!")
        self.titleLabel.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.titleLabel.setFont(QtGui.QFont("Arial", 20))
        self.titleLabel.setStyleSheet("color: blue;")

        self.messageLabel = setupLabel(self.mainLayout, "")
        self.messageLabel.setAlignment(Qt.AlignCenter)
        self.messageLabel.setFont(QtGui.QFont("Arial", 14))
        self.messageLabel.setStyleSheet("color: red;")
       
        self.inputFieldList = setupLineEdit(self.mainLayout, "Enter your userName: ")
        self.inputField = self.inputFieldList
        self.inputField.returnPressed.connect(lambda: self.on_input_submitted(self.inputField))
    
    def on_input_submitted(self, inputField):
        """Handle the input submission"""
        userName = inputField.text()
        if self.connection:
            if self.login:
                query = "SELECT * FROM Player WHERE UserName = %s"
                self.cursor.execute(query, (userName,))
                result = self.cursor.fetchone()
                if result:
                    self.currentUser.setName(result[1])
                    query = "SELECT ID FROM Player WHERE UserName = %s"
                    self.cursor.execute(query, (self.currentUser.getName(),))
                    result_id = self.cursor.fetchone()
                    if result_id:
                        self.currentUser.setId(result_id[0])
                    self.setupMainMenu()
                else:
                    QMessageBox.warning(self.main_window, "Input Error", f"Username {userName} does not exist.")
                    inputField.clear()
                    inputField.setFocus()
        else:
            self.label.setText("Database connection failed.")

    def setupCreateAccountMenu(self):
        """
        Set up the create account menu.
        """
        clear_screen(self.mainLayout)

        self.titleLabel = setupLabel(self.mainLayout, "Create your account !")
        self.titleLabel.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.titleLabel.setFont(QtGui.QFont("Arial", 20))

        self.inputLayout = setupLineEdit(self.mainLayout, "Enter your userName: ")
        self.inputField_1 = self.inputLayout

        self.mainLayout.addStretch(1)
        self.messageLabel = setupLabel(self.mainLayout, "")
        self.messageLabel.setAlignment(Qt.AlignCenter)
        self.messageLabel.setFont(QtGui.QFont("Arial", 14))
        self.mainLayout.addStretch(1)

        self.buttonList  = setupButtons(self.mainLayout, (200,50), "Create Account", "Back")
        create_account_button = self.buttonList[0]
        back_button = self.buttonList[1]
        # Connect each button to its appropriate function
        create_account_button.clicked.connect(self.createAccount)
        back_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("IntroMenu"))

    def createAccount(self):
        """Handle account creation"""
        userName = self.inputField_1.text()

        if not userName:
           QMessageBox.warning(self.main_window, "Input Error", "Please enter a username.")
           
        if userName:
            #check if the username already exists
            query = "SELECT * FROM Player WHERE UserName = %s"
            self.cursor.execute(query, (userName,))
            result = self.cursor.fetchone()
            if result:
                QMessageBox.warning(self.main_window, "Input Error", f"Username {userName} already exists.")
                self.inputField_1.clear()
                self.inputField_1.setFocus()
                return
            # Create a new Player object
            self.currentUser = Player(userName, None)
            # Insert the new player into the database
            query = "INSERT INTO Player (UserName) VALUES (%s)"
            self.cursor.execute(query, (userName,))
            self.connection.commit()

            response = QMessageBox.information(self.main_window, "Success", f"Account {userName} created successfully.")
            if response == QMessageBox.Ok:
                self.scene_manager.switch_to_menu("IntroMenu")
         
    def setupMainMenu(self):
        """
        Set up the main menu layout.
        """
        clear_screen(self.mainLayout)
        self.label = QLabel(f"Welcome back {self.currentUser.getName()} !")
        self.label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.label.setFont(QtGui.QFont("Arial", 15))
        self.label.setStyleSheet("color: blue;")
        self.mainLayout.addWidget(self.label)
        
        self.testLayout = setupLabel(self.mainLayout, "ID: ", "Character: ", "Quest: ", "Beast: ")
        self.idLabel = self.testLayout[0]
        self.idLabel.setText(f"ID: {self.currentUser.getId()}")
        self.characterLabel = self.testLayout[1]
        self.characterLabel.setText(f"Character: {self.currentUser.getCharacterSelected()}")
        self.mainLayout.addStretch(1)

        self.buttonLayout = setupVButtons(self.mainLayout, "Character", "Inventory", "NPC", "Quest", "Monster", "Log Out", "Delete Account")
        
        character_button = self.buttonLayout[0]
        inventory_button = self.buttonLayout[1]
        npc_button = self.buttonLayout[2]
        quest_button = self.buttonLayout[3]
        monster_button = self.buttonLayout[4]
        logout_button = self.buttonLayout[5]
        delete_account_button = self.buttonLayout[6]

        
        self.mainLayout.addStretch(1)
        #Connect each button to its appropriate function
        character_button.clicked.connect(self.setupCharacterMenu)
        # inventory_button.clicked.connect(self.setupInventoryMenu)
        # npc_button.clicked.connect(self.setupNPCMenu)
        # quest_button.clicked.connect(self.setupQuestMenu)
        # monster_button.clicked.connect(self.setupMonsterMenu)
        logout_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("IntroMenu"))
        delete_account_button.clicked.connect(self.deleteAccount)

        # self.mainLayout.addStretch(1)

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
                # Delete from database
                query = "DELETE FROM Player WHERE UserName = %s"
                self.cursor.execute(query, (self.currentUser.getName(),))
                self.connection.commit()
                
                QMessageBox.information(
                    self.main_window,
                    "Success",
                    f"Account '{self.currentUser.getName()}' has been deleted."
                )

                 # Clear user data
                self.currentUser = Player(None, None)

                # Switch to start menu
                self.scene_manager.switch_to_menu("IntroMenu")
            except Exception as e:
                QMessageBox.critical(
                    self.main_window,
                    "Error",
                    f"Failed to delete account: {str(e)}"
                )
    def setupCharacterMenu(self):
        """
        Set up the character menu with a scrollable list of characters.
        """
        clear_screen(self.mainLayout)
        
        # Header
        self.label = QLabel(f"Choose Your Character {self.currentUser.getName()} !")
        self.label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.label.setFont(QtGui.QFont("Arial", 15))
        self.label.setStyleSheet("color: blue;")
        self.mainLayout.addWidget(self.label)

        # Fetch characters from database
        self.currentUser.getCharacterFromDatabase()
        self.characterList = self.currentUser.getCharacterList()
        
        # Create list widget
        self.characterListLayout = QHBoxLayout()
        self.character_list = QtWidgets.QListWidget()
        # if the character name is already in the list, it will not be added again
        for character in self.characterList:
            if character.name not in [item.text() for item in self.character_list.findItems("", QtCore.Qt.MatchContains)]:
                item = QtWidgets.QListWidgetItem(character.name)
                self.character_list.addItem(item)
        self.characterListLayout.addWidget(self.character_list)
        
        # Enable context menu and double-click selection
        self.character_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.character_list.customContextMenuRequested.connect(self.showCharacterContextMenu)
        self.character_list.itemDoubleClicked.connect(self.selectCharacter)

        self.character_details = QLabel("Character Details")
        self.character_details.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.character_details.setFont(QtGui.QFont("Arial", 12))
        self.character_details.setStyleSheet("color: blue;")
        self.characterListLayout.addWidget(self.character_details)

        self.character_list.currentItemChanged.connect(self.on_item_changed)
        
        self.mainLayout.addLayout(self.characterListLayout)
        self.buttonList = setupButtons(self.mainLayout, (200, 50), "Create a new Character", "Exit")
        self.buttonList[0].clicked.connect(self.setupCreateCharacterMenu)
        self.buttonList[1].clicked.connect(lambda: self.scene_manager.switch_to_menu("Main Menu"))
       
    def showCharacterContextMenu(self, position):
        """
        Show context menu for character list items.
        """
        menu = QMenu()
        delete_action = menu.addAction("Delete Character")
        
        action = menu.exec_(self.character_list.mapToGlobal(position))
        
        if action == delete_action:
            self.deleteSelectedCharacter()

    def deleteSelectedCharacter(self):
        """
        Delete the currently selected character.
        """
        current_row = self.character_list.currentRow()
        if current_row >= 0:
            character = self.characterList[current_row]
            
            # Confirm deletion
            confirm = QMessageBox.question(
                self.main_window,
                "Confirm Deletion",
                f"Are you sure you want to delete character '{character.name}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if confirm == QMessageBox.Yes:
                try:
                    # Delete from database
                    query = "DELETE FROM `Character` WHERE CharacterName = %s AND PlayerID = %s"
                    self.cursor.execute(query, (character.name, self.currentUser.getId()))
                    self.connection.commit()
                    
                    # Remove from list
                    self.character_list.takeItem(current_row)
                    self.currentUser.removeCharacter(character)
                    
                    QMessageBox.information(
                        self.main_window,
                        "Success",
                        f"Character '{character.name}' has been deleted."
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self.main_window,
                        "Error",
                        f"Failed to delete character: {str(e)}"
                    )

    def selectCharacter(self, item):
        """
        Select the character when double-clicked.
        """
        current_row = self.character_list.currentRow()
        if current_row >= 0:
            character = self.characterList[current_row]
            self.currentUser.setCharacterSelected(character.name)
            
            QMessageBox.information(
                self.main_window,
                "Character Selected",
                f"You have selected '{character.name}' as your active character."
            )
            
            # Update character name in main menu
            self.scene_manager.switch_to_menu("Main Menu")
        
    def on_item_changed(self, current, previous):
        """
        Update the character details when an item is selected in the list.
        """
        if current:
            character = self.characterList[self.character_list.currentRow()]
            self.character_details.setText(f"""Character Details:
        Class: {character.getAttribute('classe')}
        Strength: {character.getAttribute('strength')}
        Agility: {character.getAttribute('agility')}
        Intelligence: {character.getAttribute('intelligence')}
        PV: {character.getAttribute('pv')}
        Mana: {character.getAttribute('mana')}""")
           
    def setupCreateCharacterMenu(self):
        """
        Set up the create character menu.
        """
        clear_screen(self.mainLayout)

        self.label = QLabel(f"Create your character {self.currentUser.getName()} !")
        self.label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.label.setFont(QtGui.QFont("Arial", 15))
        self.label.setStyleSheet("color: blue;")
        self.mainLayout.addWidget(self.label)

        self.inputFieldList = setupLineEdit(self.mainLayout, "Enter your character name: ")
        self.inputField = self.inputFieldList
        self.inputField.returnPressed.connect(lambda: self.on_input_submitted(self.inputField))

        self.classLayout = QHBoxLayout()
        self.classeCombobox = QtWidgets.QComboBox()
        self.classeCombobox.addItems(["Assassin", "Archer", "Barbare", "Berserker", "Chasseur","Chevalier", "Démoniste", "Druide", 
                                    "Enchanteresse", "Guerrier","Illusionniste", "Mage", "Moine", "Nécromancien", "Paladin","Prêtresse", "Rôdeur", "Sorcière", "Templier"])
        self.classeLabel = QLabel("Choose your class: ")
        self.classLayout.addWidget(self.classeLabel)
        self.classLayout.addWidget(self.classeCombobox)
        self.mainLayout.addLayout(self.classLayout)
        
        # Initialize attribute values
        self.attributes = {
            "Strength": 10,
            "Agility": 10,
            "Intelligence": 10,
            "pv": 100,
            "mana": 100
        }
        
        # Create layouts for attributes with increase/decrease buttons
        self.attributeLayouts = {}
        for attr in self.attributes:
            layout = QHBoxLayout()
            
            # Label showing attribute name and current value
            label = QLabel(f"{attr}: {self.attributes[attr]}")
            
            # Decrease button
            decreaseBtn = QPushButton("-")
            decreaseBtn.setFixedSize(30, 30)
            decreaseBtn.clicked.connect(lambda checked, a=attr: self.decreaseAttribute(a))
            
            # Increase button
            increaseBtn = QPushButton("+")
            increaseBtn.setFixedSize(30, 30)
            increaseBtn.clicked.connect(lambda checked, a=attr: self.increaseAttribute(a))
            
            # Add widgets to layout
            layout.addWidget(label)
            layout.addStretch()
            layout.addWidget(increaseBtn)
            layout.addWidget(decreaseBtn)
            
            # Store references to the label for updating
            self.attributeLayouts[attr] = {
                "layout": layout,
                "label": label
            }
            
            # Add the attribute layout to main layout
            self.mainLayout.addLayout(layout)
        
        self.mainLayout.addStretch(1)

        self.buttonList = setupButtons(self.mainLayout, (200,50), "Create Character", "Back")
        createAcc_button = self.buttonList[0]
        back_button = self.buttonList[1]

        # Connect each button to its appropriate function
        back_button.clicked.connect(self.setupCharacterMenu)
        createAcc_button.clicked.connect(self.createCharacter)

    def increaseAttribute(self, attr):
        """Increase the attribute value"""
        if self.attributes[attr] < 200:
            self.attributes[attr] += 1

        self.attributeLayouts[attr]["label"].setText(f"{attr}: {self.attributes[attr]}")
            

    def decreaseAttribute(self, attr):
        """Decrease the attribute value"""
        if self.attributes[attr] > 0:
            self.attributes[attr] -= 1
        self.attributeLayouts[attr]["label"].setText(f"{attr}: {self.attributes[attr]}")

    def createCharacter(self):
        """Handle character creation"""
        characterName = self.inputField.text()
        classe = self.classeCombobox.currentText()
        if not characterName:
            QMessageBox.warning(self.main_window, "Input Error", "Please enter a character name.")
            return

        #check if the character name already exists
        query = "SELECT * FROM `Character` WHERE CharacterName = %s"
        self.cursor.execute(query, (characterName,))
        result = self.cursor.fetchone()
        if result:
            QMessageBox.warning(self.main_window, "Input Error", f"Character {characterName} already exists.")
            self.inputField.clear()
            self.inputField.setFocus()
            return

        # Create a new Character object
        newCharacter = Character(characterName, classe, self.attributes["Strength"], self.attributes["Agility"], 
                                 self.attributes["Intelligence"], self.attributes["pv"], self.attributes["mana"])

        #Insert the new character into the database
        query = "INSERT INTO `Character` (PlayerID, CharacterName, Class, Strength, Agility, Intelligence, pv, mana) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (self.currentUser.getId(), characterName, newCharacter.getAttribute("classe"), newCharacter.getAttribute("strength"), 
                  newCharacter.getAttribute("agility"), newCharacter.getAttribute("intelligence"), 
                  newCharacter.getAttribute("pv"), newCharacter.getAttribute("mana"))
        self.cursor.execute(query, values)
        self.connection.commit()

        response = QMessageBox.information(self.main_window, "Success", f"Character {characterName} created successfully.")
        if response == QMessageBox.Ok:
            self.scene_manager.switch_to_menu("Character")
from gui.utils import *
from loadFiles import *
import sys
from gui.Component import *

class MainWindow(QMainWindow):
    """
    Main application window.
    This class sets up the main window and its components.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPG Game")
        self.setGeometry(100, 100, 800, 600)
        self.mainLayout = QVBoxLayout()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.mainLayout)
        self.user = None
        self.id = None
        self.characterName = None
        self.login = False
        self.setupStartMenu()
        self.connection = connectToDatabase()
        self.cursor = self.connection.cursor()
      

    def setupStartMenu(self):
        """
        Set up the main menu layout.
        """
        clear_screen(self.mainLayout)

        self.titleLabel = setupLabel(self.mainLayout, "Welcome to the RPG Game!")
        self.titleLabel.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.titleLabel.setFont(QtGui.QFont("Arial", 20))
        self.titleLabel.setStyleSheet("color: blue;")
        
        self.buttonList = setupButtons(self.mainLayout, (200,50), "Log In", "Create Account")
        # Connect each button to its appropriate function
        login_button = self.buttonList[0]
        create_account_button = self.buttonList[1]
        
        login_button.clicked.connect(self.setupLogInMenu)
        create_account_button.clicked.connect(self.setupCreateAccountMenu)
         

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
        back_button.clicked.connect(self.setupStartMenu)

    def setupMainMenu(self):
        """
        Set up the main menu layout.
        """
        clear_screen(self.mainLayout)
        self.label = QLabel(f"Welcome back {self.user} !")
        self.label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.label.setFont(QtGui.QFont("Arial", 15))
        self.label.setStyleSheet("color: blue;")
        self.mainLayout.addWidget(self.label)
        
        self.testLayout = setupLabel(self.mainLayout, "ID: ", "Character: ", "Quest: ", "Beast: ")
        self.idLabel = self.testLayout[0]
        self.idLabel.setText(f"ID: {self.id}")
        self.characterLabel = self.testLayout[1]
        self.characterLabel.setText(f"Character: {self.characterName}")
        self.mainLayout.addStretch(1)

        self.buttonLayout = setupVButtons(self.mainLayout, "Character", "Inventory", "NPC", "Quest", "Monster", "Log Out")
        
        character_button = self.buttonLayout[0]
        inventory_button = self.buttonLayout[1]
        npc_button = self.buttonLayout[2]
        quest_button = self.buttonLayout[3]
        monster_button = self.buttonLayout[4]
        
        self.mainLayout.addStretch(1)
        #Connect each button to its appropriate function
        character_button.clicked.connect(self.setupCharacterMenu)
        # inventory_button.clicked.connect(self.setupInventoryMenu)
        # npc_button.clicked.connect(self.setupNPCMenu)
        # quest_button.clicked.connect(self.setupQuestMenu)
        # monster_button.clicked.connect(self.setupMonsterMenu)

        # self.mainLayout.addStretch(1)

    def createAccount(self):
        """Handle account creation"""
        userName = self.inputField_1.text()
        # classe = self.classeCombobox.currentText()

        if not userName:
            self.messageLabel.setStyleSheet("color: red;")
            self.messageLabel.setText("Please fill in all fields.")
        if userName:
            self.messageLabel.setStyleSheet("color: green;")
            self.messageLabel.setText(f"Account {userName} created successfully.")
          
            query = "INSERT INTO Player (UserName) VALUES (%s)"
            self.cursor.execute(query, (userName,))
            self.connection.commit()
            self.messageLabel.setText(f"Account {userName} created successfully.")
        else:
            self.label.setText("Database connection failed.")

    def setupCharacterMenu(self):
        """
        Set up the character menu.
        """
        clear_screen(self.mainLayout)
        self.label = QLabel(f"Choose Your Character {self.user} !")
        self.label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.label.setFont(QtGui.QFont("Arial", 15))
        self.label.setStyleSheet("color: blue;")
        self.mainLayout.addWidget(self.label)

        query = "SELECT * FROM `Character` WHERE PlayerID = %s"
        self.cursor.execute(query, (self.id,))
        
        # Get column names from cursor.description
        columns = [desc[0] for desc in self.cursor.description]
        
        
        # Fetch all rows (use fetchall instead of fetchone to get multiple rows)
        results = self.cursor.fetchall()
        
        if results:
            # Create a layout for character data
            character_data = QVBoxLayout()
            
            for result in results:
                for i, col_name in enumerate(columns):
                    data_row = QHBoxLayout()
                    col_label = QLabel(f"{col_name}:")
                    col_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
                    value_label = QLabel(str(result[i]))
                    if col_name == "CharacterName":
                        data_row.addWidget(col_label)
                        data_row.addWidget(value_label)
                        data_row.addStretch()  # This pushes everything that follows to the right
                        self.buttonList = setupButtons(data_row, (80,20), "Select", "Delete")
                        self.buttonList[0].clicked.connect(lambda _, name=result[i]: self.selectCharacter(name))
                        self.buttonList[1].clicked.connect(lambda _, name=result[i]: self.deleteCharacter(name))
                    else:
                        data_row.addWidget(col_label)
                        data_row.addWidget(value_label)
                        data_row.addStretch()
                    
                    character_data.addLayout(data_row)
                
                character_data.addSpacing(10)  # Add space between characters if multiple
                
            character_widget = QWidget()
            character_widget.setLayout(character_data)
            
            # Add to a scroll area in case there's a lot of data
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(character_widget)
            
            self.mainLayout.addWidget(scroll)
        else:
            no_char_label = QLabel("No character found")
            no_char_label.setAlignment(Qt.AlignCenter)
            self.mainLayout.addWidget(no_char_label)

        self.mainLayout.addStretch(1)
        self.messageLabel = setupLabel(self.mainLayout, "")
        self.messageLabel.setAlignment(Qt.AlignCenter)
        self.messageLabel.setFont(QtGui.QFont("Arial", 14))
        self.mainLayout.addStretch(1)

        self.buttonList = setupButtons(self.mainLayout, (200,50), "Create a character", "Back")
        createAcc_button = self.buttonList[0]
        back_button = self.buttonList[1]
        # Connect each button to its appropriate function
        back_button.clicked.connect(self.setupMainMenu)
        createAcc_button.clicked.connect(self.setupCreateCharacterMenu)
    
    def setupCreateCharacterMenu(self):
        """
        Set up the create character menu.
        """
        clear_screen(self.mainLayout)

        self.label = QLabel(f"Create your character {self.user} !")
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
        print("Character created successfully with name:", characterName,"and ID:", self.id)
        print("Class:", classe)
        for attr, value in self.attributes.items():
            print(f"{attr}: {value}")
        # if not characterName:
        #     self.messageLabel.setStyleSheet("color: red;")
        #     self.messageLabel.setText("Please fill in all fields.")
        # else:
        #     self.messageLabel.setStyleSheet("color: green;")
        #     self.messageLabel.setText(f"Character {characterName} created successfully.")
        #     query = "INSERT INTO `Character` (PlayerID, CharacterName, Class) VALUES (%s, %s, %s)"
        #     self.cursor.execute(query, (self.id, characterName, classe))
        #     self.connection.commit()
        #     self.characterName = characterName
        #     self.setupCharacterMenu()
    
    def selectCharacter(self, characterName):
        self.characterName = characterName
        self.messageLabel.setStyleSheet("color: green;")
        self.messageLabel.setText(f"Character {self.characterName} selected successfully.")

    def on_input_submitted(self, inputField):
        """Handle the input submission"""
        userName = inputField.text()
        if self.connection:
            if self.login:
                query = "SELECT * FROM Player WHERE UserName = %s"
                self.cursor.execute(query, (userName,))
                result = self.cursor.fetchone()
                if result:
                    self.user = userName
                    query = "SELECT ID FROM Player WHERE UserName = %s"
                    self.cursor.execute(query, (self.user,))
                    result_id = self.cursor.fetchone()
                    if result_id:
                        self.id = result_id[0]
                    self.setupMainMenu()
                else:
                    self.messageLabel.setText(f"User {userName} not found.")
                    inputField.clear()
                    inputField.setFocus()
        else:
            self.label.setText("Database connection failed.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
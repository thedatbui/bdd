from utils import *


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
        self.login = False
        self.setupStartMenu()

    def setupStartMenu(self):
        """
        Set up the main menu layout.
        """
        clear_screen(self.mainLayout)

        self.titleLabel = setupLabel(self.mainLayout, "Welcome to the RPG Game!")
        self.titleLabel.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.titleLabel.setFont(QtGui.QFont("Arial", 20))
        self.titleLabel.setStyleSheet("color: blue;")
        
        self.buttonList = setupButtons(self.mainLayout, "Log In", "Create Account")
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

        self.inputLayout = setupLineEdit(self.mainLayout, "Enter your userName: ", "Enter your character name: ")
        self.inputField_1 = self.inputLayout[0]
        self.inputField_2 = self.inputLayout[1]

        self.classLayout = QHBoxLayout()
        self.classeCombobox = QtWidgets.QComboBox()
        self.classeCombobox.addItems(["Guerrier", "Mage", "Voleur", "Archer", "Assassin"])
        self.classeLabel = QLabel("Choose your class: ")
        self.classLayout.addWidget(self.classeLabel)
        self.classLayout.addWidget(self.classeCombobox)
        self.mainLayout.addLayout(self.classLayout)

        self.mainLayout.addStretch(1)
        self.messageLabel = setupLabel(self.mainLayout, "")
        self.messageLabel.setAlignment(Qt.AlignCenter)
        self.messageLabel.setFont(QtGui.QFont("Arial", 14))
        self.mainLayout.addStretch(1)

        self.buttonList  = setupButtons(self.mainLayout, "Create Account", "Back")
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
        
        self.testLayout = setupLabel(self.mainLayout, "Character: ", "Quest: ", "Beast: ")
        self.testLayout.setAlignment(Qt.AlignHCenter)
        
        self.mainLayout.addStretch(1)
        
        self.buttonLayout = setupVButtons(self.mainLayout, "Character", "Inventory", "NPC", "Quest", "Monster")
        
        character_button = self.buttonLayout[0]
        inventory_button = self.buttonLayout[1]
        npc_button = self.buttonLayout[2]
        quest_button = self.buttonLayout[3]
        monster_button = self.buttonLayout[4]
        
        self.mainLayout.addStretch(1)
        # Connect each button to its appropriate function
        # character_button.clicked.connect(self.setupCharacterMenu)
        # inventory_button.clicked.connect(self.setupInventoryMenu)
        # npc_button.clicked.connect(self.setupNPCMenu)
        # quest_button.clicked.connect(self.setupQuestMenu)
        # monster_button.clicked.connect(self.setupMonsterMenu)

        # self.mainLayout.addStretch(1)

    def createAccount(self):
        """Handle account creation"""
        userName = self.inputField_1.text()
        characterName = self.inputField_2.text()
        classe = self.classeCombobox.currentText()

        if not userName or not characterName:
            self.messageLabel.setStyleSheet("color: red;")
            self.messageLabel.setText("Please fill in all fields.")
        if userName and characterName:
            self.messageLabel.setStyleSheet("color: green;")
            self.messageLabel.setText(f"Account {userName} created successfully.")
        
        # if connection:
        #     cursor = connection.cursor()
        #     query = "INSERT INTO Player (UserName, CharacterName, Class) VALUES (%s, %s, %s)"
        #     cursor.execute(query, (userName, characterName, classe))
        #     connection.commit()
        #     cursor.close()
        #     connection.close()
        #     self.messageLabel.setText(f"Account {userName} created successfully.")
        # else:
        #     self.label.setText("Database connection failed.")

    def on_input_submitted(self, inputField):
        """Handle the input submission"""
        userName = inputField.text()
        print(userName)
        connection = connectToDatabase()
        if connection:
            if self.login:
                cursor = connection.cursor()
                query = "SELECT * FROM Player WHERE UserName = %s"
                cursor.execute(query, (userName,))
                result = cursor.fetchone()
                if result:
                    self.user = userName
                    self.setupMainMenu()
                else:
                    self.messageLabel.setText(f"User {userName} not found.")
                cursor.close()
                connection.close()
        else:
            self.label.setText("Database connection failed.")

   
    

if __name__ == "__main__":
    # Load CSV file
    # main()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
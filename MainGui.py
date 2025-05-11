from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QScrollArea, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import sys
from gui.Component import *
from gui.utils import setMenuState
from gui.MenuManager import SceneManager
import loadFiles as loadFiles
import loadFiles as loadFiles
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
    
        setMenuState("IntroMenu")
        self.sceneManager = SceneManager(self)
        self.sceneManager.set_scene()
        print("Scene set up successfully")


if __name__ == "__main__":
    # loadFiles.main()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
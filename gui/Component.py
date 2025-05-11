from gui.utils import *

class TitleComponent:
    @staticmethod
    def create(layout, text):
        title = QLabel(text)
        title.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        title.setFont(QtGui.QFont("Arial", 20))
        title.setStyleSheet("color: blue;")
        layout.addWidget(title)
        return title

class ButtonComponent:
    @staticmethod
    def create(layout, text, size=(200, 50), on_click=None):
        button = QPushButton(text)
        button.setFixedSize(size[0], size[1])
        button.setStyleSheet("background-color: lightblue; font-size: 16px;")
        if on_click:
            button.clicked.connect(on_click)
        layout.addWidget(button)
        return button

class QlineEditComponent:
    @staticmethod
    def create(layout, placeholder_text, size=(200, 50)):
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        line_edit.setFixedSize(size[0], size[1])
        line_edit.setStyleSheet("font-size: 16px;")
        layout.addWidget(line_edit)
        return line_edit
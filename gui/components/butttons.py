from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt

def create_button(text, size=(200, 50), style=None):
    """
    Create a button with the specified text, size, and style.
    
    Returns:
        QPushButton: The created button.
    """
    button = QPushButton(text)
    button.setFixedSize(size[0], size[1])
    
    # Apply default style if none provided
    if style is None:
        style = "background-color: lightblue; font-size: 16px;"
    
    button.setStyleSheet(style)
    return button

def add_horizontal_buttons(layout, size=(200, 50), *button_texts):
    """
    Create buttons in a horizontal layout and add them to the parent layout.
    
    Args:
        layout: The parent layout to add buttons to
        size: Button size as (width, height)
        button_texts: Variable number of strings for button texts
        
    Returns:
        list: List of created buttons
    """
    h_layout = QHBoxLayout()
    h_layout.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
    buttons = []
    
    for text in button_texts:
        button = create_button(text, size)
        h_layout.addWidget(button)
        buttons.append(button)
    
    layout.addLayout(h_layout)
    return buttons if len(buttons) > 1 else buttons[0]

def add_vertical_buttons(layout, size=(200, 50), *button_texts):
    """
    Create buttons in a vertical layout and add them to the parent layout.
    
    Args:
        layout: The parent layout to add buttons to
        size: Button size as (width, height)
        button_texts: Variable number of strings for button texts
        
    Returns:
        list: List of created buttons
    """
    v_layout = QVBoxLayout()
    v_layout.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
    buttons = []
    
    for text in button_texts:
        button = create_button(text, size)
        v_layout.addWidget(button)
        buttons.append(button)
    
    layout.addLayout(v_layout)
    return buttons if len(buttons) > 1 else buttons[0]
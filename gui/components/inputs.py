from PyQt5.QtWidgets import QLineEdit, QHBoxLayout, QLabel, QComboBox
from PyQt5.QtCore import Qt

def create_line_edit(placeholder_text="", size=None):
    """
    Create a QLineEdit widget with the specified placeholder text.
    """
    line_edit = QLineEdit()
    line_edit.setPlaceholderText(placeholder_text)
    if size:
        line_edit.setFixedSize(size[0], size[1])
    line_edit.setStyleSheet("font-size: 16px;")
    return line_edit

def add_labeled_input(layout, label_text, placeholder_text=""):
    """
    Add a labeled input field to the layout.
    
    Returns the created QLineEdit.
    """
    h_layout = QHBoxLayout()
    
    label = QLabel(label_text)
    label.setStyleSheet("font-size: 16px;")
    h_layout.addWidget(label)
    
    line_edit = create_line_edit(placeholder_text)
    h_layout.addWidget(line_edit)
    
    layout.addLayout(h_layout)
    return line_edit

def create_combobox(items=None):
    """
    Create a combobox with the specified items.
    """
    combo = QComboBox()
    if items:
        combo.addItems(items)
    return combo

def add_labeled_combobox(layout, label_text, items=None):
    """
    Add a labeled combobox to the layout.
    
    Returns the created QComboBox.
    """
    h_layout = QHBoxLayout()
    
    label = QLabel(label_text)
    label.setStyleSheet("font-size: 16px;")
    h_layout.addWidget(label)
    
    combo = create_combobox(items)
    h_layout.addWidget(combo)
    
    layout.addLayout(h_layout)
    return combo
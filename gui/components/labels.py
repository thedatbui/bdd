from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt

def create_title_label(text, font_size=20, color="blue", alignment=None):
    """
    Create a label styled as a title.
    """
    label = QLabel(text)
    if alignment:
        label.setAlignment(alignment)
    else:
        label.setAlignment(Qt.AlignTop | Qt.AlignCenter)
    
    label.setFont(QtGui.QFont("Arial", font_size))
    label.setStyleSheet(f"color: {color};")
    return label

def create_label(text, font_size=15, color="blue", alignment=None):
    """
    Create a standard label.
    """
    label = QLabel(text)
    if alignment:
        label.setAlignment(alignment)
    
    label.setFont(QtGui.QFont("Arial", font_size))
    if color:
        label.setStyleSheet(f"color: {color};")
    return label

def add_horizontal_labels(layout, *text_list):
    """
    Create labels in a horizontal layout and add them to the parent layout.
    """
    h_layout = QHBoxLayout()
    labels = []
    
    for text in text_list:
        label = create_label(text)
        h_layout.addWidget(label)
        labels.append(label)
    
    layout.addLayout(h_layout)
    return labels if len(labels) > 1 else labels[0]

def add_vertical_labels(layout, *text_list):
    """
    Create labels in a vertical layout and add them to the parent layout.
    """
    v_layout = QVBoxLayout()
    labels = []
    
    for text in text_list:
        label = create_label(text)
        v_layout.addWidget(label)
        labels.append(label)
    
    layout.addLayout(v_layout)
    return labels if len(labels) > 1 else labels[0]
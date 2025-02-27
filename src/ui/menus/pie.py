import sys
from math import pi, cos, sin
from PySide6.QtCore import Qt, QPointF, QTimer, QEvent
from PySide6.QtGui import QCursor, QGuiApplication
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton

from quilt.widget import Widget
from quilt.layout import orbit, VBoxLayout

class PieMenu(Widget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.setFramelessWindow(True)
        self.setTransparentWindow(True)
        self.setFloatingWindow(True)
        self.setWindowFlag(Qt.Tool, True)  # Set as a tool window (stays above main window)
        self.setWindowModality(Qt.ApplicationModal)  # Ensure it blocks interaction with other windows

        # Install event filter to catch all events
        self.installEventFilter(self)

        # Create a list of buttons
        self.layout = VBoxLayout()
        for i in range(10):  # Number of buttons to be arranged
            button = QPushButton(f"{i + 1}", self)
            button.setFixedSize(30, 30)
            button.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border-radius: 15px;
                }

                QPushButton:hover {
                    background-color: red;
                }

            """)
            # Replace close with a custom action for each button
            button.clicked.connect(lambda i=i: self.on_button_click(i))  
            self.layout.structure.append(button)

        self.setLayout(self.layout)

    
    def showEvent(self, event):
        pos = QCursor.pos()
        self.setGeometry(pos.x() - 125, pos.y() - 125, 250, 250),
        orbit(self.layout.structure, QPointF(self.width() / 2, self.height() / 2), 100)
        return super().showEvent(event)

    def closeEvent(self, event):
        return super().closeEvent(event)

    def leaveEvent(self, event):
        return super().leaveEvent(event)

    # Custom function to handle button click
    def on_button_click(self, i):
        self.close()
        print(f"Button {i} clicked")
        # Perform specific action for button click, like emitting a signal or changing state.

    # Override eventFilter to intercept mouse events
    def eventFilter(self, obj, event):
        return super().eventFilter(obj, event)

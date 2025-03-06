import sys
import keyboard  # For global hotkey
import time
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QWindow
import pygetwindow as gw  # To track window focus

class PopupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Popup Window")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        self.button = QPushButton("Close Window")
        self.button.clicked.connect(self.hide_and_return)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.previous_window = None

    def show_and_remember(self):
        """Remember the currently active window before showing."""
        self.previous_window = gw.getActiveWindow()  # Get currently active window
        self.show()
        self.activateWindow()

    def hide_and_return(self):
        """Hide and return focus to the previous app."""
        self.hide()
        time.sleep(0.1)  # Small delay to ensure window focus can switch

        if self.previous_window:
            try:
                self.previous_window.activate()  # Bring back the original window
            except Exception:
                print("Failed to restore window focus")

def show_window():
    if not window.isVisible():
        window.show_and_remember()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PopupWindow()

    # Set a global hotkey (e.g., "shift+space" to open the window)
    keyboard.add_hotkey("space", show_window)

    sys.exit(app.exec())

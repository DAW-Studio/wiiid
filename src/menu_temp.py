import socket
import threading
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMenu
from PySide6.QtCore import QThread, QTimer

from quilt.widget import MenuApp


class ToolWindow(QMenu):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tool Window")
        self.resize(300, 200)

        self.addAction("eiujfnwijeknfwejklbnf")


if __name__ == "__main__":
    app = QApplication([])
    window = ToolWindow()
    window.show()
    app.exec()

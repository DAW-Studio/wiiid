import socket
import threading
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import QThread, QTimer

from quilt.widget import MenuApp


class ToolWindow(MenuApp):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tool Window")
        self.resize(300, 200)

        self.setFloatingWindow(True)

        self.button = QPushButton("MENU", self)
        self.button.clicked.connect(self.sendData)
        layout = QVBoxLayout(self)
        layout.addWidget(self.button)

    def sendData(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("127.0.0.1", 5001))  # Localhost on port 5000
        self.client.sendall(b"From Menu")
        response = self.client.recv(1024).decode()
        if not response:
            pass
        else:
            self.show()
            self.button.setText(response)
        self.client.close()

if __name__ == "__main__":
    app = QApplication([])
    window = ToolWindow()
    window.show()
    app.exec()

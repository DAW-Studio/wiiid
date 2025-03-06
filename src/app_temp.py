import sys
import socket
import subprocess
import threading
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout
from PySide6.QtCore import QThread

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main App")
        self.resize(300, 200)

        self.button = QPushButton("Open Tool & Send Data", self)
        self.button.clicked.connect(self.sendData)

        layout = QVBoxLayout(self)
        layout.addWidget(self.button)

        subprocess.Popen(["./dist/WiiiDMenus.app/Contents/MacOS/WiiiDMenus"])
        self.send_to_menu = False

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("127.0.0.1", 5001))  # Localhost on port 5000

        self.server_thread = threading.Thread(target=self.startServer, daemon=True)
        # self.server_thread = QThread()
        # self.server_thread.started.connect(self.startServer)
        self.server_thread.start()

    def startServer(self):
        self.server.listen(1)
        while True:
            client, _ = self.server.accept()
            message = client.recv(1024).decode()
            self.show()
            self.button.setText(message)
            client.close()

    def sendData(self):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("127.0.0.1", 5001))  # Connect to the Tool App
            client.sendall(b"From Main")
            client.close()
        except ConnectionRefusedError:
            print("Tool App is not running!")


if __name__ == "__main__":
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec()


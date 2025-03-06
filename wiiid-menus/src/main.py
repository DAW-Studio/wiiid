import sys
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer
import time

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)  # Prevent app from quitting if no windows are open

# Create a simple window
window = QWidget()
window.setWindowTitle("MacOS Tool")
window.setWindowFlags(Qt.Tool)  # Makes it behave like a tool (no dock icon, etc.)
window.setWindowFlag(Qt.FramelessWindowHint, True)
window.setAttribute(Qt.WA_TranslucentBackground, True)

layout = QHBoxLayout()

box = QLabel("TEST")
box.setFixedSize(window.width(),window.height())
box.setStyleSheet("""
    background-color: red;
    border-radius: 50px;
""")

layout.addWidget(box)

window.setLayout(layout)

# window.show()
# window.hide()
# window.show()

QTimer().singleShot(3000, window.show)
QTimer().singleShot(3100, window.raise_)
QTimer().singleShot(3100, window.activateWindow)
QTimer().singleShot(6000, QApplication.quit) 


sys.exit(app.exec())

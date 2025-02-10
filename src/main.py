# main.py
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from wiimote.interface import WiiiD

def main():
    app = QApplication([])
    # window = MainWindow(wiiid)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
# main.py
import sys
import os

# sys.path.append(os.path.dirname(__file__))

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
# from wiimote.interface import WiiiD
from ui.menus.pie import PieMenu
from quilt.debug import HotReload

def main():
    app = QApplication([])
    app.setStyleSheet("background-color:white;")
    # window = MainWindow(wiiid)
    window = MainWindow()
    window.show()

    # window.pie_menu = PieMenu(window)
    # window.pie_menu.show()
    

    # HotReload(window, "<cmd>+s", before=window.wiiid.close).start()
    HotReload(window, "<cmd>+s").start()

    app.exec()

if __name__ == "__main__":
    main()

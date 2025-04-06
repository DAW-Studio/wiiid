# main.py
import sys
import os

# sys.path.append(os.path.dirname(__file__))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow
# from wiimote.interface import WiiiD
from ui.menus.pie import PieMenu
from quilt.debug import HotReload

QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

def main():
    app = QApplication([])
    with open("resources/style.css") as f:
        app.setStyleSheet(f.read())
    # window = MainWindow(wiiid)
    window = MainWindow()
    window.show()

    # window.pie_menu = PieMenu(window)
    # window.pie_menu.show()
    

    # HotReload(window, "<cmd>+<esc>", before=window.wiiid.close).start()
    HotReload(window, "<cmd>+<esc>").start()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

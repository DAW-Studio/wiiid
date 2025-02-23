# main.py
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
# from wiimote.interface import WiiiD
from quilt.debug import HotReload

def main():
    app = QApplication([])
    # window = MainWindow(wiiid)
    window = MainWindow()
    window.show()

    # HotReload(window, before=window.wiiid.close).start()
    HotReload(window, "<cmd>+s").start()

    app.exec()

if __name__ == "__main__":
    main()

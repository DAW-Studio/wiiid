from PySide6 import QtCore, QtWidgets, QtGui
import sys
import json
import time

from ui.app import Window


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = Window()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())

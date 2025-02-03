from types import NoneType
from PySide6 import QtCore, QtWidgets, QtGui
import sys
import json
import os
import time

from wiihid import Wiimote

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # APP UI
        self.setWindowTitle("WiiiD")
        pallete = self.palette()
        pallete.setColor(self.backgroundRole(), "#ffffff")
        self.setPalette(pallete)

        # UI
        layout = QtWidgets.QVBoxLayout()

        self.text = QtWidgets.QLabel("output", alignment=QtCore.Qt.AlignCenter)
        self.text.setStyleSheet("color: #000000;")
        layout.addWidget(self.text)

        self.setLayout(layout)

        # WIIMOTE
        self.wiimote = Wiimote()
        self.buttons = {}
        for btn in "ab12-+h<>^v":
            self.buttons[btn] = Button(btn)
        self.buttonsHeld = []
        with open("wiiid/config.json", "r") as f:
            self.config = json.load(f)
        

    @QtCore.Slot()
    def connect_wiimote(self):
        self.wiimote.data.connect(self.process_wiimote_data)
        time.sleep(1)
        self.wiimote.start()


    def process_wiimote_data(self, data):
        data = json.loads(data)

        # for button in self.wiimoteWidget.selected.keys():
        #     if button in ["<", ">", "^", "v"]:
        #         unselected = self.wiimoteWidget.unselected["dpad"]
        #     else:
        #         unselected = self.wiimoteWidget.unselected[button]
        #     selected = self.wiimoteWidget.selected[button]
        #     if data[button] and not selected.isVisible():
        #         selected.setVisible(True)
        #         unselected.setVisible(False)
        #     elif not data[button] and selected.isVisible():
        #         selected.setVisible(False)
        #         unselected.setVisible(True)

        # for btn, value in data.items():
        #     button = self.buttons[btn]
        #     state = button.state(value)
        #     if state != None:
        #         action, args = state
        #         try:
        #             config = self.config[action][args]
        #             actions.run[config["device"]][config["action"]](button, config["args"])
        #         except KeyError as e:
        #             print("KeyError:", e)


    
    def close(self):
        self.wiimote.quit()
        sys.exit()


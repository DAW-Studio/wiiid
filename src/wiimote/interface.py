# src/wiimote/controller.py
import sys
import time
import json
import os
from . import WiiHid, WiiHidError, Button, actions
from PySide6.QtCore import QThread, Signal


def resource_path(path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.path.abspath("."), path)


class WiiiD(QThread):
    signal = Signal(list)
    def __init__(self, parent, wiimote_widget) -> None:
        super().__init__()
        self.parent = parent
        self.wiimote_widget = wiimote_widget
        self.debug = False
        self.buttons = {}
        for b in ["up","down","left","right","a","b","home","minus","plus","1","2"]:
            self.buttons[b] = Button(self, b, self.wiimote_widget)
        self.heldButtons = []
        self.currentMap = 0
        with open(resource_path("resources/mappings.json")) as f:
            self.config = json.load(f)

    def run(self):
        if not self.connect_():
            sys.exit()
        self.wii.rumble(.05)
        self.setLeds(self.config["leds"][self.currentMap])
        while True:
            btnState = self.wii.state()
            if btnState != None:
                for btn in self.buttons:
                    button = self.buttons[btn]
                    state = button.state(btnState[btn])
                    if state != None:
                        self.signal.emit([button])
                        self.act(button, state)
            # time.sleep(0.01)

    def setLeds(self, leds):
        self.wii.leds = leds
        self.wiimote_widget.leds = leds

    def act(self, button, state):
        action, btn = state
        if action == "tap" and btn == "home":
            self.currentMap += 1 if self.currentMap != len(self.config["leds"])-1 else -self.currentMap
            pl = self.wii.leds
            self.wii.leds = self.config["leds"][self.currentMap]
            if pl == [0,0,0,0]:
                time.sleep(.5)
                self.setLeds([0,0,0,0])

        elif action == "hold" and btn == "home":
            if self.debug:
                self.debug = False
                self.setLeds([0,0,0,0])
            else:
                self.debug = True
                self.setLeds([1,1,1,1])
            # if self.wii.leds == [0,0,0,0]:
            #     self.wii.leds = self.config["leds"][self.currentMap]
            # else:
            #     self.wii.leds = [0,0,0,0]
        try:
            if self.debug:
                mapping = self.config["mappings"][-1][action][btn]
                exec(mapping)
            else:
                mapping = self.config["mappings"][self.currentMap][action][btn]
                if mapping["device"] == "wiiid":
                    self.signal.emit([mapping])
                else:
                    actions.run[mapping["device"]][mapping["action"]](self, button, mapping["args"])
        except KeyError as e:
            print(e)
        
    def connect_(self):
        while True:
            try:
                self.wii = WiiHid()
                break
            except WiiHidError as e:
                print(e)
            time.sleep(1)
        return True

    def close(self):
        self.wii.close()

import sys
import wiihid
import time
import json
import os
from button import Button
import actions


class Wiiid:
    def __init__(self) -> None:
        if not self.connect():
            sys.exit()
        self.wii.rumble(.2)
        self.debug = False
        self.buttons = {
            "a": Button(self, "a"),
            "b": Button(self, "b"),
            "up": Button(self, "up"),
            "down": Button(self, "down"),
            "left": Button(self, "left"),
            "right": Button(self, "right"),
            "plus": Button(self, "plus"),
            "minus": Button(self, "minus"),
            "home": Button(self, "home"),
            "1": Button(self, "1"),
            "2": Button(self, "2")
        }
        self.heldButtons = []
        self.currentMap = 0
        with open(f"config.json") as f:
            self.config = json.load(f)
        self.wii.leds = self.config["leds"][self.currentMap]


    def run(self):
        while True:
            btnState = self.wii.state()
            if btnState != None:
                for btn in self.buttons:
                    button = self.buttons[btn]
                    state = button.state(btnState[btn])
                    if state != None:
                        self.act(button, state)
            # time.sleep(0.01)


    def act(self, button, state):
        action, btn = state
        if action == "tap" and btn == "home":
            self.currentMap += 1 if self.currentMap != len(self.config["leds"])-1 else -self.currentMap
            pl = self.wii.leds
            self.wii.leds = self.config["leds"][self.currentMap]
            if pl == [0,0,0,0]:
                time.sleep(.5)
                self.wii.leds = [0,0,0,0]

        elif action == "hold" and btn == "home":
            if self.debug:
                self.debug = False
                self.wii.leds = [0,0,0,0]
            else:
                self.debug = True
                self.wii.leds = [1,1,1,1]
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
                actions.run[mapping["device"]][mapping["action"]](self, button, mapping["args"])
        except KeyError as e:
            print(e)
        
    def connect(self):
        while True:
            try:
                self.wii = wiihid.Wii()
                break
            except wiihid.WiiHidError as e:
                print(e)
            time.sleep(1)
        return True


if __name__ == "__main__":
    Wiiid().run()
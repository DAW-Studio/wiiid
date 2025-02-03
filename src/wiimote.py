import sys
import wiihid
import time
import json
import os
from button import Button


class Wiiid:
    def __init__(self) -> None:
        if not self.connect():
            sys.exit()
        self.wii.rumble(.2)
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
        # with open(f"config.json") as f:
        #     self.config = json.load(f)


    def run(self):
        while True:
            btnState = self.wii.state()
            if btnState != None:
                for btn in self.buttons:
                    button = self.buttons[btn]
                    state = button.state(btnState[btn])
                    if state != None:
                        self.act(button, state)
            time.sleep(0.1)


    def act(self, btn, state):
        print(state)
        # # try:
        # #     config = self.config[action][args]
        # #     actions.run[config["device"]][config["action"]](btn, *config["args"])
        # # except KeyError as e:
        #     print(e)
        
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
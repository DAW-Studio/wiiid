import time
import json
from . import Keyboard, KeyCode


k = Keyboard()
# m = Mouse()

class Debug():
    def __init__(self):
        pass

    def reloadConf(self, wiiid):
        with open("src/config.json") as f:
           wiiid.config = json.load(f) 
        print("Reloaded Config")


class KeyboardDevice():
    def __init__(self) -> None:
        pass

    def tap(self, wiiid, btn, args:dict):
        key, mod = args["key"], args["mod"]
        k.tap(key, mod)

    def hold(self, wiiid, btn, args:dict):
        key, mod = args["key"], args["mod"]
        k.press(key, mod)
        try:
            duration = args["duration"]
            time.sleep(duration)
            k.release()
        except KeyError:
            pass

    
    def release(self, wiiid, btn, args:dict):
        key, mod = args["key"], args["mod"]
        k.release()

    def cycle(self, wiiid, btn, args:dict):
        keys = args["keys"] 
        key, mods = keys[btn.cycle]
        k.tap(key, mods)
        btn.cycle += 1
        if btn.cycle == len(keys):
            btn.cycle = 0
    
    def type(self, wiiid, btn, args:dict):
        text, delay = args["text"], args["delay"]
        k.type(text, delay)


# class MouseDevice():
#     def __init__(self) -> None:
#         pass

#     def click(self, btn, button:str, double:bool):
#         print(button, double)

#     def hold(self, btn, button:str, duration:bool):
#         print(button, duration)

#     def move(self, btn, point:tuple, speed:int):
#         print(point, speed)
    
#     def drag(self, btn, pointA:tuple, pointB:tuple, speed:int):
#         print(pointA, pointB, speed)

#     def scroll(self, btn, direction:str, amount:int, speed:int):
#         print(direction, amount, speed)


# class WiiidDevice():
#     def __init__(self) -> None:
#         pass
    
#     def delay(self, btn, duration:float):
#         time.sleep(1)

#     def macro(self, btn, actions:list):
#         for m in actions:
#             run[m["device"]][m["action"]](btn,*m["args"])


debug = Debug()
kd = KeyboardDevice()
# md = MouseDevice()
# wd = WiiidDevice()
run = {
    "keyboard": {
        "tap": kd.tap,
        "hold": kd.hold,
        "release": kd.release,
        "cycle": kd.cycle,
        "type": kd.type
    }#,
    # "mouse": {
    #     "click": md.click,
    #     "hold": md.hold,
    #     "move": md.move,
    #     "drag": md.drag,
    #     "scroll": md.scroll
    # },
    # "wiiid": {
    #     "delay": wd.delay,
    #     "macro": wd.macro
    # }
}
from pynput.keyboard import Key, KeyCode, Controller
from pynput.mouse import Controller as MouseController


mods = {
    "shift": Key.shift,
    "ctrl": Key.ctrl,
    "alt": Key.alt,
    "win": Key.cmd,
    "cmd": Key.cmd,
}

keys = {
    "shift": Key.shift,
    "space": Key.space
}


class Keyboard(Controller):
    def __init__(self) -> None:
        super().__init__()
    
    def tap(self, key, mod="") -> None:
        if key in keys: key = keys[key]
        if mod != "":
            mod = mods[mod]
            super().press(mod)
            super().tap(key)
            super().release(mod)
        else:
            super().tap(key)

    def press(self, key, mod="") -> None:
        if key in keys: key = keys[key]
        if mod != "":
            mod = mods[mod]
            super().press(mod)
            super().press(key)
            super().release(mod)
        else:
            super().press(key)
    
    def release(self, key, mod: str | Key | KeyCode="") -> None:
        if key in keys: key = keys[key]
        if mod != "":
            super().release(mod)
        super().release(key)


class Mouse(MouseController):
    def __init__(self) -> None:
        super().__init__()

    def move(self, dx: int, dy: int) -> None:
        return super().move(dx, dy)

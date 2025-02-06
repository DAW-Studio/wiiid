from pynput.keyboard import Key, KeyCode, Controller

mods = {
    "shift": Key.shift,
    "ctrl": Key.ctrl,
    "alt": Key.alt,
    "win": Key.cmd,
    "cmd": Key.cmd,
}

class Keyboard(Controller):
    def __init__(self) -> None:
        super().__init__()
    
    def tap(self, key: str | Key | KeyCode, mod: str | Key | KeyCode="") -> None:
        if mod != "":
            mod = mods[mod]
            super().press(mod)
            super().tap(key)
            super().release(mod)
        else:
            super().tap(key)

    def press(self, key: str | Key | KeyCode, mod: str | Key | KeyCode="") -> None:
        if mod != "":
            mod = mods[mod]
            super().press(mod)
            super().press(key)
            super().release(mod)
        else:
            super().press(key)
    
    def release(self, key: str | Key | KeyCode, mod: str | Key | KeyCode="") -> None:
        if mod != "":
            super().release(mod)
        super().release(key)
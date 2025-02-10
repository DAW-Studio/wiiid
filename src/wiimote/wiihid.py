# src/wiimote/wiihid.py
import hid
import time


BTN_A = 2048
BTN_B = 1024
BTN_1 = 512
BTN_2 = 256
BTN_PLUS = 16
BTN_MINUS = 4096 
BTN_HOME = 32768
BTN_LEFT = 1
BTN_RIGHT = 2
BTN_DOWN = 4
BTN_UP = 8


class WiiHidError(Exception):
    def __init__(self, message, available=[]):
        super().__init__(message)
        self.available = available


class WiiHid:
    def __init__(self) -> None:
        connected = False
        devices = hid.enumerate()
        for device in devices:
            if device["product_string"].lower().find("nintendo") != -1:
                vendor_id = device["vendor_id"]
                product_id = device["product_id"]
                connected = True
                break

        if not connected:
            error = "No Wiimotes detected"
            raise WiiHidError(error, available=devices)
        else:
            self.device = hid.Device(vendor_id, product_id)
            self.prev_data = 0
            self.device.write(bytes([0x52, 0x15, 0x00]))
            time.sleep(0.1)
            data = self.device.read(32)
            self._leds = [0,0,0,0]
    
    def state(self):
        try:
            data = self.device.read(32)
        except hid.HIDException as e:
            error = "Wiimote disconnected"
            raise WiiHidError(error)
        data = data[1]|data[2]<<8
        if data == 0 and self.prev_data == 0:
            return None
        self.prev_data = data
        buttons = {
            "a": (data & BTN_A) != 0 ,
            "b": (data & BTN_B) != 0,
            "1": (data & BTN_1) != 0,
            "2": (data & BTN_2) != 0,
            "plus": (data & BTN_PLUS) != 0,
            "minus": (data & BTN_MINUS) != 0,
            "home": (data & BTN_HOME) != 0,
            "left": (data & BTN_LEFT) != 0,
            "right": (data & BTN_RIGHT) != 0,
            "down": (data & BTN_DOWN) != 0,
            "up": (data & BTN_UP) != 0
        }
        return buttons
    
    def rumble(self, seconds:float=0.3):
        rumble_on = [0x52, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] 
        rumble_off = [0x52, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.device.write(bytes(rumble_on))
        time.sleep(seconds)
        self.device.write(bytes(rumble_off))

    @property
    def leds(self):
        return self._leds
    
    @leds.setter
    def leds(self, l:list[int,int,int,int]):
        l1 = 0x10 if l[0] == 1 else 0x00
        l2 = 0x20 if l[1] == 1 else 0x00
        l3 = 0x40 if l[2] == 1 else 0x00
        l4 = 0x80 if l[3] == 1 else 0x00
        self.device.write(bytes([0x11, l1|l2|l3|l4]))
        self._leds = l

    def close(self):
        self.device.close()
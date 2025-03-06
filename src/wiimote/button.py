import time

class Button:
    def __init__(self, wiiid, name:str, wiimote_widget, value:int=0, time:float=-1):
        self.wiiid = wiiid
        self.name = name
        self.wiimote_widget = wiimote_widget
        self.value = value
        self.time = time
        self.cycle = 0
        self.holding = False

    def state(self, btnState:bool):
        if btnState:
            if self.value == 0:
                self.pressed()
            if self.time != -1 and time.time()-self.time > .5 and not self.holding:
                self.wiiid.heldButtons.append(self)
                return self.hold()
        elif self.value == 1:
            return self.released()
        return None

    def pressed(self):
        self.wiimote_widget.activate(self.name)
        self.value = 1
        self.time = time.time()

    def released(self):
        self.wiimote_widget.deactivate(self.name)
        self.value = 0
        self.time = -1
        if not self.holding:
            return ["tap", self.name]
        else:
            self.holding = False
            self.wiiid.heldButtons.remove(self)
            return ["release", self.name]

    def hold(self):
        self.time = -1
        self.holding = True
        return ["hold", self.name] 
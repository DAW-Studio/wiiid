import time

class Button:
    def __init__(self, wiiid, name:str, value:int=0, time:float=-1):
        self.name = name
        self.value = value
        self.time = time
        self.cycle = 0

    def state(self, btnState:bool):
        if btnState:
            if self.value == 0:
                self.pressed()
        elif self.value == 1:
            return self.released()
        if self.time != -1 and time.time() - self.time > 0.5:
            return self.held()
        return None

    def pressed(self):
        self.value = 1
        self.time = time.time()

    def released(self):
        self.value = 0
        self.time = -1
        return ["tap", self.name]

    def held(self):
        self.time = -1
        # return ["hold", self.name] 
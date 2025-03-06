import os
import time

from PySide6.QtWidgets import (
    QWidget,
    QGraphicsWidget,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsPixmapItem
)
from PySide6.QtGui import (
    QPixmap,
    QBrush,
    QColor
)
from PySide6.QtCore import (
    Qt,
    QTimer
)

from quilt.core import loop

# IMPLEMENT GRAPHICS WIDGET INTO QUILT
# HAVING A WIDGET + A SCENE + A VIEW IS OVERKILL

ACTIVE="resources/images/wiimote/active/"
INACTIVE="resources/images/wiimote/inactive/"

class WiimoteWidget():
    def __init__(self):
        self.scene = QGraphicsScene()
        front = QGraphicsPixmapItem(QPixmap("./resources/images/wiimote/front.png"))
        front.setScale(.35)
        back = QGraphicsPixmapItem(QPixmap("./resources/images/wiimote/back.png"))
        back.setScale(.35)
        self.scene.addItem(back)

        self.dpad = ["up","down","left","right"]
        self.active = {}
        self.inactive = {}
        for state, dict_ in ((ACTIVE, self.active), (INACTIVE, self.inactive)):
            for file in os.listdir(state):
                pixmap = QGraphicsPixmapItem(QPixmap(state+file))
                pixmap.setScale(.35)
                if state == ACTIVE: pixmap.hide()
                name = file.split(".")[0]
                dict_[name] = pixmap
                self.scene.addItem(dict_[name])

        self.scene.addItem(front)

        self.view = QGraphicsView()
        self.view.setScene(self.scene)
        self.view.setStyleSheet("background-color: white;")
        self.view.setBackgroundBrush(QBrush(QColor("white")))
        
        self._leds = [0,0,0,0]
        
        self.leds = [1,1,0,0]
        # self.activate("led3")

        self.blink_state = 0
        # self.blinkLeds()


    def activate(self, name):
        self.view.viewport().update()
        print("ACTIVATE ", name)
        if name in self.dpad:
            self.inactive["dpad"].setVisible(False)
            for d in self.dpad:
                self.active[d].setVisible(False)
        else:
            self.inactive[name].setVisible(False)
        self.active[name].setVisible(True)
    
    def deactivate(self, name):
        self.view.viewport().update()
        if name in self.dpad:
            self.inactive["dpad"].setVisible(True)
        else:
            self.inactive[name].setVisible(True)
        self.active[name].setVisible(False)
    
    @property
    def leds(self):
        return self._leds
    
    @leds.setter
    def leds(self, l:list):
        for i, state in enumerate(l):
            led = f"led{i+1}"
            self.activate(led) if state == 1 else self.deactivate(led)
        self._leds = l

    @loop(200)
    def blinkLeds(self):
        v = (True, False) if self.blink_state else (False, True)
        # self.wiiid.wii.leds = [0,0,0,0] if self.blink_state else [1,1,1,1]
        self.blink_state = 0 if self.blink_state else 1
        for state, visible in ((self.inactive, v[0]), (self.active, v[1])):
            for i in range(1,5):
                state[f"led{i}"].setVisible(visible)
            



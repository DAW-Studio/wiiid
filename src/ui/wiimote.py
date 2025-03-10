import os
import time

from PySide6.QtWidgets import (
    QWidget,
    QGraphicsWidget,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsPixmapItem,
    QSizePolicy
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

from quilt.layout import VBoxLayout
from quilt.core import loop


# IMPLEMENT GRAPHICS WIDGET INTO QUILT
# HAVING A WIDGET + A SCENE + A VIEW IS OVERKILL

ACTIVE="resources/images/wiimote/active/"
INACTIVE="resources/images/wiimote/inactive/"


class WiimoteGraphicsView(QGraphicsView):
    def __init__(self, parent, scene):
        super().__init__(scene)
        self.setScene(scene)
        self.parent = parent
        self.setObjectName("wiimote-graphics-view")
        self.setBackgroundBrush(QBrush(QColor("white")))
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setContentsMargins(0,0,0,0)
        # self.scene().setSceneRect(0, 0, self.width(), self.height())
        # for i in self.scene().items():
        #     i.setScale(.35)
            # i.setPos(self.scene().width()/2, self.scene().height()/2)
            # self.scene().removeItem(i)
            # self.scene().addItem(i)

    def resizeEvent(self, event):
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
        super().resizeEvent(event)


class WiimoteWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("wiimote-widget")
        # self.setStyleSheet("background: black;")
        self.scene = QGraphicsScene()
        back = QGraphicsPixmapItem(QPixmap("./resources/images/wiimote/back.png"))
        self.scene.addItem(back)

        self.dpad = ["up","down","left","right"]
        self.active = {}
        self.inactive = {}
        for state, dict_ in ((ACTIVE, self.active), (INACTIVE, self.inactive)):
            for file in os.listdir(state):
                pixmap = QGraphicsPixmapItem(QPixmap(state+file))
                if state == ACTIVE: pixmap.hide()
                name = file.split(".")[0]
                dict_[name] = pixmap
                self.scene.addItem(dict_[name])

        front = QGraphicsPixmapItem(QPixmap("./resources/images/wiimote/front.png"))
        self.scene.addItem(front)

        self.view = WiimoteGraphicsView(self, self.scene)
        self.setLayout(VBoxLayout([
            self.view
        ]))
        
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
            



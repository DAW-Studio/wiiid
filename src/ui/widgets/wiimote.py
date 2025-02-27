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

# IMPLEMENT GRAPHICS WIDGET INTO QUILT
# HAVING A WIDGET + A SCENE + A VIEW IS OVERKILL

ACTIVE="resources/images/wiimote/active/"
INACTIVE="resources/images/wiimote/inactive/"

class WiimoteWidget():
    def __init__(self, wiiid):
        self.wiiid = wiiid
        scene = QGraphicsScene()
        full = QGraphicsPixmapItem(QPixmap("./resources/images/wiimote/full.png"))
        # full.setTransformationMode(Qt.FastTransformation)
        full.setScale(.35)
        scene.addItem(full)

        self.active = {}
        self.inactive = {}
        for state, dict_ in ((ACTIVE, self.active), (INACTIVE, self.inactive)):
            for file in os.listdir(state):
                pixmap = QGraphicsPixmapItem(QPixmap(state+file))
                pixmap.setScale(.35)
                if state == ACTIVE: pixmap.hide()
                name = file.split(".")[0]
                dict_[name] = pixmap
                scene.addItem(dict_[name])
        
        for i in range(1,5):
            self.active[f"led{i}"].show()
            self.inactive[f"led{i}"].hide()

        self.timer = QTimer()
        self.timer.timeout.connect(self.search)
        self.timer.start(200)
        self.led_state = 0

        self.view = QGraphicsView()
        self.view.setScene(scene)
        self.view.setStyleSheet("background-color: white;")
        self.view.setBackgroundBrush(QBrush(QColor("white")))

    def search(self):
        v = (True, False) if self.led_state else (False, True)
        # self.wiiid.wii.leds = [0,0,0,0] if self.led_state else [1,1,1,1]
        self.led_state = 0 if self.led_state else 1
        for state, visible in ((self.inactive, v[0]), (self.active, v[1])):
            for i in range(1,5):
                state[f"led{i}"].setVisible(visible)
            



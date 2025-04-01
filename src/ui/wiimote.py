import os

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QStackedLayout,
    QVBoxLayout
)
from PySide6.QtGui import (
    QPixmap
)
from PySide6.QtCore import (
    Qt,
    QSize
)


ACTIVE="resources/images/wiimote/active/"
INACTIVE="resources/images/wiimote/inactive/"


class WiimoteWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("wiimote-widget")

        self.pixmaps = {}

        self.back = QLabel(self, pixmap=QPixmap("./resources/images/wiimote/back.png"))
        self.pixmaps[self.back] = self.back.pixmap() 

        self.dpad = ["up","down","left","right"]
        self.active = {}
        self.inactive = {}
        for state, dict_ in ((ACTIVE, self.active), (INACTIVE, self.inactive)):
            for file in os.listdir(state):
                pixmap = QPixmap(state+file)
                label = QLabel(self, pixmap=pixmap)
                if state == ACTIVE: label.hide()
                name = file.split(".")[0]
                dict_[name] = label
                self.pixmaps[label] = pixmap

        self.front = QLabel(self, pixmap=QPixmap("./resources/images/wiimote/front.png"))
        self.pixmaps[self.front] = self.front.pixmap() 

        self._leds = [0,0,0,0]
        self.leds = [1,1,0,0]

        self.update_image_sizes()

    def resizeEvent(self, event):
        self.update_image_sizes()
        super().resizeEvent(event)

    def update_image_sizes(self):
        height = self.height()  

        for label, pixmap in self.pixmaps.items():
            scaled = pixmap.scaledToHeight(height, Qt.SmoothTransformation)
            label.setPixmap(scaled)
            label.resize(scaled.size())

        new_width = self.back.width()+ 40
        self.resize(new_width, height)

        for label in self.pixmaps.keys():
            label.move((new_width - label.width())//2, 0)

    def activate(self, name):
        print("ACTIVATE ", name)
        if name in self.dpad:
            self.inactive["dpad"].setVisible(False)
            for d in self.dpad:
                self.active[d].setVisible(False)
        else:
            self.inactive[name].setVisible(False)
        self.active[name].setVisible(True)
    
    def deactivate(self, name):
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

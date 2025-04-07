from PySide6 import QtCore
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QGraphicsDropShadowEffect,
    QGraphicsBlurEffect,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QGraphicsView,
    QSizePolicy
)
from PySide6.QtCore import (
    QTimer,
    Qt,
    QPoint,
    QRect,
    QEvent
)
from PySide6.QtGui import (
    QMouseEvent,
    QColor,
    QPixmap,
    QPainter,
    QBrush,
    QPen
)
import time
# from wiimote.interface import WiiiD
import os

from quilt.widget import MainCustomWindow
from quilt.layout import VBoxLayout, HBoxLayout
from quilt.core import loop

from wiimote.interface import WiiiD

from ui.titlebar import TitleBar
from ui.menus.pie import PieMenu
from ui.wiimote import WiimoteWidget
from ui.mapping import Mapping


# class WiimoteWidget:
#     def __init__(self) -> None:
#         scene = QGraphicsScene()
#         body_back_image = QGraphicsPixmapItem(QPixmap("src/resources/images/wiimote/body_back.png"))
#         scene.addItem(body_back_image)

#         self.unselected = {}
#         for i in os.listdir("src/resources/images/wiimote/unselected"):
#             if i.endswith(".png"):
#                 btn = i.strip(".png")
#                 self.unselected[btn] = QGraphicsPixmapItem(QPixmap(f"src/resources/images/wiimote/unselected/{i}"))
#                 scene.addItem(self.unselected[btn])

#         self.selected = {}
#         for i in os.listdir("src/resources/images/wiimote/selected"):
#             if i.endswith(".png"):
#                 btn = i.strip(".png")
#                 self.selected[btn] = QGraphicsPixmapItem(QPixmap(f"src/resources/images/wiimote/selected/{i}"))
#                 self.selected[btn].setVisible(False)
#                 scene.addItem(self.selected[btn])

#         body_front_image = QGraphicsPixmapItem(QPixmap("src/resources/images/wiimote/body_front.png"))
#         scene.addItem(body_front_image)
        

#         self.graphicsView = QGraphicsView()

#         self.graphicsView.setScene(scene)
#         self.graphicsView.setStyleSheet("background: white;")
#         # self.graphicsView.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("white")))



class CircularButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #D73F3F; border: none;")
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(215, 63, 63)))  # Color #D73F3F
        painter.setPen(Qt.NoPen)  # No border
        painter.drawEllipse(0, 0, self.width(), self.height())
        painter.end()


class BurgerButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #D73F3F; border: none;")
        self.clicked.connect(self.onClick)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        width = self.width()
        height = self.height()
        line_height = 1  

        painter.setPen(QPen(Qt.black, line_height))
        painter.drawLine(width * 0.2, height * 0.2, width * 0.8, height * 0.2)  # Top line
        painter.drawLine(width * 0.2, height * 0.5, width * 0.8, height * 0.5)  # Middle line
        painter.drawLine(width * 0.2, height * 0.8, width * 0.8, height * 0.8)  # Bottom line
        painter.end()

    def onClick(self):
        print("Burger menu clicked!")


class MainWindow(MainCustomWindow):
    def __init__(self):
        super().__init__()

        self.wiimote_widget = WiimoteWidget()
        self.wiiid = WiiiD(self, self.wiimote_widget)
        self.interface()

        self.setTransparentWindow(True)
        self.setFloatingWindow(True)
        geometry = self.envGeometry()
        if not geometry: geometry = QRect(100,100,650,700)
        self.setGeometry(geometry)

        self.central_widget = QWidget()

        title_bar = TitleBar(self)
        status_bar = QWidget()
        status_bar.setFixedHeight(10)
        status_bar.setObjectName("status-bar")

        self.wiimote_section = QWidget()
        self.wiimote_section.setLayout(VBoxLayout([
            title_bar,
            self.wiimote_widget,
            status_bar
        ]))
        # QTimer.singleShot(1, lambda: self.wiimote_section.setFixedWidth(self.wiimote_widget.width()))

        self.mapping_widget = Mapping(self)

        self.central_widget.setLayout(HBoxLayout([
            self.wiimote_section,
            self.mapping_widget,
        ], alignment=Qt.AlignmentFlag.AlignLeft))

        self.setCentralWidget(self.central_widget)



        self.pie_menu = PieMenu(self)

        # WiiiD

    def resizeEvent(self, event):
        self.wiimote_section.setFixedWidth(self.wiimote_widget.width())
        super().resizeEvent(event)

    def moveEvent(self, event):
        pos = event.pos()
        # if not self.screen().geometry().contains(pos.x()+self.width(), 0):
        #     if not self.main_layout.reversed:
        #         self.main_layout.reversed = True
        #         self.main_layout.structure.reverse()
        #         self.main_layout.structure = self.main_layout.structure
        #         self.setGeometry(self.x()-self.mapping_widget.width(),self.y(),self.width(),self.height())
        # elif self.main_layout.reversed:
        #     self.main_layout.reversed = False
        #     self.main_layout.structure.reverse()
        #     self.main_layout.structure = self.main_layout.structure
        return super().moveEvent(event)

    @QtCore.Slot()
    def interface(self):
        self.wiiid.signal.connect(self.process_wiiid_data)
        self.wiiid.start()

    def process_wiiid_data(self, data):
        if isinstance(data[0], dict):
            if data[0]["action"] == "pie":
                self.pie_menu.show()
        else: 
            # print(data[0])
            btn = data[0].name
            # print(btn)
            if btn == "left":
                self.wiiid.setLeds([0,0,0,0])
            if btn == "right":
                self.wiiid.setLeds([1,0,1,0])

        # for button in self.wiimoteWidget.selected.keys():
        #     if button in ["left", "right", "up", "down"]:
        #         unselected = self.wiimoteWidget.unselected["dpad"]
        #     else:
        #         unselected = self.wiimoteWidget.unselected[button]
        #     selected = self.wiimoteWidget.selected[button]
        #     if btn and not selected.isVisible():
        #         selected.setVisible(True)
        #         unselected.setVisible(False)
        #     elif not btn and selected.isVisible():
        #         selected.setVisible(False)
        #         unselected.setVisible(True)

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
    QGraphicsView
)
from PySide6.QtCore import Qt, QPoint 
from PySide6.QtGui import (
    QMouseEvent,
    QColor,
    QPixmap,
    QPainter,
    QBrush,
    QPen
)
import time
from wiimote.interface import WiiiD
import os


class WiimoteWidget:
    def __init__(self) -> None:
        scene = QGraphicsScene()
        body_back_image = QGraphicsPixmapItem(QPixmap("src/resources/images/wiimote/body_back.png"))
        scene.addItem(body_back_image)

        self.unselected = {}
        for i in os.listdir("src/resources/images/wiimote/unselected"):
            if i.endswith(".png"):
                btn = i.strip(".png")
                self.unselected[btn] = QGraphicsPixmapItem(QPixmap(f"src/resources/images/wiimote/unselected/{i}"))
                scene.addItem(self.unselected[btn])

        self.selected = {}
        for i in os.listdir("src/resources/images/wiimote/selected"):
            if i.endswith(".png"):
                btn = i.strip(".png")
                self.selected[btn] = QGraphicsPixmapItem(QPixmap(f"src/resources/images/wiimote/selected/{i}"))
                self.selected[btn].setVisible(False)
                scene.addItem(self.selected[btn])

        body_front_image = QGraphicsPixmapItem(QPixmap("src/resources/images/wiimote/body_front.png"))
        scene.addItem(body_front_image)
        

        self.graphicsView = QGraphicsView()

        self.graphicsView.setScene(scene)
        self.graphicsView.setStyleSheet("background: white;")
        # self.graphicsView.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("white")))



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


class TitleBar(QWidget):
    """Custom title bar with a centered search bar, perfectly aligned with macOS buttons."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(28)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: white; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; border-bottom: .5px solid #959595")


        layout = QHBoxLayout()
        layout.setContentsMargins(12, 0, 12, 0)  
        layout.setSpacing(0)

        self.close_button = CircularButton(self)
        self.close_button.setFixedSize(12, 12)

        self.menuButton = BurgerButton(self)
        self.menuButton.setFixedSize(18,13)

        layout.addWidget(self.close_button)
        layout.addSpacing(10) 

        layout.addStretch()

        self.title = QLabel(self)
        self.title.setText("WiiiD")
        self.title.setStyleSheet("color: #959595; font: Menlo;")
        layout.addWidget(self.title)

        layout.addStretch()

        layout.addWidget(self.menuButton, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

    def mousePressEvent(self, event: QMouseEvent):
        """Allow window dragging from the custom title bar."""
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle window movement."""
        if event.buttons() == Qt.LeftButton:
            self.window().move(self.window().pos() + event.globalPosition().toPoint() - self._drag_pos)
            self._drag_pos = event.globalPosition().toPoint()
            event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove default title bar
        self.setAttribute(Qt.WA_TranslucentBackground)  # Enable transparency for rounded corners
        self.setGeometry(100, 100, 1200, 800)

        self.title_bar = TitleBar(self)
        self.setContentsMargins(0,0,0,0)

        # Main content area
        main_content = QWidget()
        main_content.setStyleSheet("background-color: rgba(255, 255, 255, 255); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(90)  # Soft shadow like macOS
        shadow.setXOffset(0)
        shadow.setColor(QColor(0, 0, 0))  # Light black shadow

        # Apply a blur effect to the background
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(100)  # Adjust the blur radius for desired effect

        container = QWidget()
        container.setLayout(QVBoxLayout())
        container.layout().setContentsMargins(0, 0, 0, 0)
        container.layout().setSpacing(0)
        container.layout().addWidget(self.title_bar)
        container.layout().addWidget(main_content)
        container.setStyleSheet("border-radius: 12px; background-color: rgba(255, 255, 255, 180);")  # Rounded edges with transparency
        container.setGraphicsEffect(shadow)  # Apply shadow effect

        # Apply the blur effect to the container widget
        container.setGraphicsEffect(blur_effect)

        self.wiimoteWidget = WiimoteWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.wiimoteWidget.graphicsView)
        container.layout().addChildLayout(layout)

        self.setCentralWidget(container)
        self.wiiid = WiiiD()
        self.interface()

        # WiiiD
    @QtCore.Slot()
    def interface(self):
        self.wiiid.signal.connect(self.process_wiiid_data)
        self.wiiid.start()

    def process_wiiid_data(self, data):
        btn = data[0].name
        for button in self.wiimoteWidget.selected.keys():
            if button in ["left", "right", "up", "down"]:
                unselected = self.wiimoteWidget.unselected["dpad"]
            else:
                unselected = self.wiimoteWidget.unselected[button]
            selected = self.wiimoteWidget.selected[button]
            if btn and not selected.isVisible():
                selected.setVisible(True)
                unselected.setVisible(False)
            elif not btn and selected.isVisible():
                selected.setVisible(False)
                unselected.setVisible(True)
        print(btn)



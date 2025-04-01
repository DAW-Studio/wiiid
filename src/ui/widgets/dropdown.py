from PySide6.QtWidgets import (
    QPushButton,
    QWidget
)
from PySide6.QtCore import (
    Qt
)


class Widget(QWidget):
    def __init__(self, dropdown):
        super().__init__()
        self.dropdown = dropdown
        self.setWindowFlag(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    def activate(self):
        self.setFixedWidth(self.dropdown.width())
        self.show()
        self.raise_()
        self.move(self.dropdown.mapToGlobal(self.dropdown.rect().bottomLeft()))


class DropDown(QPushButton):
    def __init__(self, text="Button"):
        super().__init__(text)
        self.widget = Widget(self)
        self.clicked.connect(self.widget.activate)


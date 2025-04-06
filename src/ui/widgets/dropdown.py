from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget
)
from PySide6.QtCore import (
    QPoint,
    Qt,
    QEvent
)


class Widget(QLabel):
    def __init__(self, window, dropdown):
        super().__init__(window)
        self.dropdown = dropdown
        # self.setWindowFlag(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    def event(self, event: QEvent, /) -> bool:
        if event.type() == QEvent.WindowDeactivate:
            self.hide()
        return super().event(event)

    def activate(self):
        self.setFixedSize(self.dropdown.width(), 100)
        # self.show()
        self.resize(100,100)
        self.raise_()
        self.setVisible(True)
        self.move(self.dropdown.mapTo(self.window(), self.dropdown.rect().bottomLeft()))


class DropDown_(QPushButton):
    def __init__(self, text="Button"):
        super().__init__(text)
        # self.widget = Widget(self)

        popover = Widget(self.window(), self)
        popover.setStyleSheet("background-color: black;")
        popover.hide()

        self.clicked.connect(popover.activate)

class DropDown(QWidget):
    def __init__(self, parent, button):
        super().__init__(parent, Qt.Window | Qt.FramelessWindowHint)  
        self.button = button
        self.setAttribute(Qt.WA_TranslucentBackground)  
        self.setStyleSheet("background: white; border: 1px solid black; padding: 5px;")
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Option 1"))
        layout.addWidget(QLabel("Option 2"))
        layout.addWidget(QLabel("Option 3"))
        self.setLayout(layout)
        
    def showDropdown(self):
        parent_pos = self.button.mapToGlobal(QPoint(0, self.button.height()))
        self.move(parent_pos)
        self.raise_()
        self.show()

    def focusOutEvent(self, event):
        self.hide()


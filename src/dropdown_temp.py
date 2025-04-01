import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QListWidget,
    QAbstractItemView
)
from PySide6.QtCore import (
    Qt,
)

from quilt.widget import QMainWindow, Widget
from quilt.debug import HotReload
from quilt.layout import VBoxLayout

class DropdownWidget(QListWidget):
    def __init__(self, parent:QPushButton, items:list[str]):
        super().__init__()
        self.dropdown = parent
        self.setFixedSize(100,100)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.addItems(items)

    def mouseReleaseEvent(self, e):
        item = self.selectedItems()[0]
        self.dropdown.select(item)
        self.hide()
        return super().mouseReleaseEvent(e)

    def showEvent(self, event):
        self.setFixedWidth(self.dropdown.width())
        pos = self.dropdown.mapToGlobal(self.dropdown.rect().bottomLeft())
        pos.setY(pos.y()-5)
        self.move(pos)
        self.setFocus()
        return super().showEvent(event)

    def focusOutEvent(self, event):
        self.hide()
        return super().focusOutEvent(event)


class Dropdown(QPushButton):
    def __init__(self, parent, items:list[str]):
        super().__init__(parent=parent, text=items[0])
        self.widget = DropdownWidget(self, items)
        self.clicked.connect(self.widget.show)

    def select(self, item):
        self.setText(item.text())


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.dropdown = Dropdown(self, ["Item 1", "Item 2", "Item 3", "Item 4", "Item 1", "Item 2", "Item 3", "Item 4"])
        self.btn = QPushButton(parent=self, text="Item 0")

        self.setLayout(VBoxLayout([
            self.btn,
            self.dropdown
        ], alignment=Qt.AlignmentFlag.AlignCenter))



if __name__ == "__main__":
    app = QApplication()

    window = Window()
    window.show()

    HotReload(window, "<cmd>+s").start()

    sys.exit(app.exec())

    
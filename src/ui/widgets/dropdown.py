from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QMenu,
    QWidgetAction,
)
from PySide6.QtGui import (
    QIcon,
    QTransform,
    QPixmap
)
from PySide6.QtCore import (
    Qt
)

from quilt.layout import VBoxLayout, HBoxLayout

# (icon path, name, action)

class Menu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        # self.setGeometry(100,100,100,100)
        self.setStyleSheet("""
            QMenu {
                background-color: #171B24;
            }
            QMenu::item {
                height: 30px;
                padding-top: 8px;
                padding-bottom: 8px;
            }
        """)
        self.setItems()
    
    # ICON DOESNT SHOW
    def setItems(self):
        for action in self.actions():
            self.removeAction(action)
        for i, item in enumerate(self.parent().items):
            if i != self.parent().selected:
                widget = QLabel("TEST")
                widget.setStyleSheet("background-color: red;")
                widget_action = QWidgetAction(self)
                widget_action.setDefaultWidget(widget)
                widget_action.triggered.connect(lambda _, index=i: self.parent().select(index))
                self.addAction(widget_action)
            # action.triggered.connect(lambda _, o=option: self.select_option(o))

    def showEvent(self, event):
        self.update()
        self.setFixedWidth(self.parent().width())
        self.parent().flipArrow()
        return super().showEvent(event)

    def closeEvent(self, event):
        self.parent().flipArrow()
        return super().closeEvent(event)


class DropDown(QPushButton):
    def __init__(self, parent, items:list[tuple], selected=0):
        super().__init__(items[0])
        self.items = items
        self.selected = selected
        self.setFixedHeight(50)
        self.setStyleSheet("""
            QPushButton {
                background: #171B24;
                border: none;
            }
            QPushButton:hover {
                background: #12161D;
            }
            QPushButton:focus {
                background: #0E1016;
            }
            QPushButton::menu-indicator {
                image: none;
            }
        """)
        # self.clicked.connect(self.open)
        self.setMenu(Menu(self))

        # self.icon_label = QPushButton()
        # self.icon_label.setStyleSheet("background: transparent;")
        # self.icon_label.setIconSize(self.icon_label.sizeHint())
        # self.name_label = QLabel()
        # self.name_label.setStyleSheet("background: transparent;")
        # self.arrow_label = QPushButton(icon=QIcon("assets/icons/dropdown/arrow.svg"))
        # self.arrow_label.setIconSize(self.arrow_label.sizeHint()*.25)
        # self.arrow_label.setStyleSheet("background: transparent;")
        # self.setLayout(HBoxLayout([
        #     self.icon_label,
        #     self.name_label,
        #     {"stretch": 1},
        #     self.arrow_label
        # ], contents_margins=(10,0,10,0)))

        # self.select(selected)

    def select(self, index:int):
        # i = self.items[index] if index != -1 else self.items[self.selected]
        i = self.items[index]
        self.icon_label.setIcon(QIcon(i[0]))
        self.name_label.setText(i[1])
        self.selected = index
        self.menu().setItems()

    def mousePressEvent(self, event):
        self.menu().updateGeometry()
        self.menu().setFixedWidth(self.width())
        return super().mousePressEvent(event)

    def flipArrow(self):
        pixmap = self.arrow_label.icon().pixmap(self.arrow_label.iconSize())
        flipped = pixmap.transformed(QTransform().scale(1,-1))
        self.arrow_label.setIcon(QIcon(flipped))

from PySide6.QtWidgets import (
    QWidget,
)
from PySide6.QtCore import (
    Qt,
)

from quilt.layout import VBoxLayout, HBoxLayout

from ui.widgets.dropdown import DropDown

class ToolBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.dropdown = DropDown(self, [
            QA
        ])

        self.setLayout(HBoxLayout([
            self.dropdown
        ]))


class Mapping(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("mapping-widget")
        # self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.toolbar = ToolBar(self)

        self.setLayout(VBoxLayout([
            self.toolbar
        ], alignment=Qt.AlignmentFlag.AlignTop))

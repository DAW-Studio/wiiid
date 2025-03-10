from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel
)
from PySide6.QtGui import (
    QMouseEvent
)
from PySide6.QtCore import (
    Slot,
    Qt
)

from quilt.layout import HBoxLayout

class CloseButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(12,12)
        self.setObjectName("close-button")
        self.clicked.connect(self.onClick)
        self.setStyleSheet(f"border-radius: {self.width()/2};")

    @Slot()
    def onClick(self, event):
        QApplication.quit()
    


class TitleBar(QWidget):
    """Custom title bar with a centered search bar, perfectly aligned with macOS buttons."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(32)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("title-bar")

        self.title = QLabel("WiiiD")
        self.title.setObjectName("title")

        layout = HBoxLayout([
            CloseButton(),
            {"stretch": 1},
            self.title,
            {"stretch": 1}
        ])
        layout.setContentsMargins(12, 0, 12, 0)  

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
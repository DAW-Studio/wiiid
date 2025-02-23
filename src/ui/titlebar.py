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
        self.setStyleSheet("background-color: red;")
        self.clicked.connect(self.onClick)

    @Slot()
    def onClick(self, event):
        QApplication.quit()
    


class TitleBar(QWidget):
    """Custom title bar with a centered search bar, perfectly aligned with macOS buttons."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(28)
        # self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: white; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; border-bottom: .5px solid #959595")

        self.title = QLabel(self)
        self.title.setText("WiiiD")
        self.title.setStyleSheet("color: #959595; font: Menlo;")

        layout = HBoxLayout([
            CloseButton(),
            {"stretch": 1},
            self.title,
            {"stretch": 1}
        ])
        layout.setContentsMargins(12, 0, 12, 0)  

        # # self.menuButton = BurgerButton(self)
        # # self.menuButton.setFixedSize(18,13)

        # layout.addWidget(self.close_button)
        # layout.addSpacing(10) 

        # layout.addStretch()


        # layout.addStretch()

        # layout.addWidget(self.menuButton, alignment=Qt.AlignmentFlag.AlignRight)

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
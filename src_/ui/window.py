from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect, QGraphicsBlurEffect, QLabel
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QMouseEvent, QColor, QPixmap, QPainter, QBrush, QPen


class CircularButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #D73F3F; border: none;")
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set the button background color and shape (circular)
        painter.setBrush(QBrush(QColor(215, 63, 63)))  # Color #D73F3F
        painter.setPen(Qt.NoPen)  # No border
        painter.drawEllipse(0, 0, self.width(), self.height())
        
        painter.end()



class MenuButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #D73F3F; border: none;")
    
    def paintEvent(self, event):
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QBrush(QColor(0,0,0)))
        painter.setPen(Qt.NoPen)
        painter.drawLine(0,0,self.width(),self.height())
        painter.drawLine(0,self.height()/2,self.width(),self.height())
        painter.drawLine(0,self.height(),self.width(),self.height())
        painter.end()



class BurgerButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setFixedSize(50, 50)  # Set button size
        self.setStyleSheet("background-color: #D73F3F; border: none;")
        
        # Connect the clicked signal to the onClick method
        self.clicked.connect(self.onClick)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.Antialiasing)
        
        # Calculate proportional sizes
        width = self.width()
        height = self.height()
        line_height = 1  # Line thickness proportional to the height

        # Set pen with white color and proportional line thickness
        painter.setPen(QPen(Qt.black, line_height))
        
        # Draw the three lines, centered horizontally and spaced vertically
        painter.drawLine(width * 0.2, height * 0.2, width * 0.8, height * 0.2)  # Top line
        painter.drawLine(width * 0.2, height * 0.5, width * 0.8, height * 0.5)  # Middle line
        painter.drawLine(width * 0.2, height * 0.8, width * 0.8, height * 0.8)  # Bottom line
        
        painter.end()

    def onClick(self):
        # Show a message when the burger button is clicked
        print("Burger menu clicked!")

class CustomTitleBar(QWidget):
    """Custom title bar with a centered search bar, perfectly aligned with macOS buttons."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(28)  # Standard macOS title bar height
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: white; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; border-bottom: .5px solid #959595")


        layout = QHBoxLayout()
        layout.setContentsMargins(12, 0, 12, 0)  # Adjust margins to align correctly
        layout.setSpacing(0)

        # Left-side macOS buttons (Fake, just for alignment)
        self.close_button = CircularButton(self)
        self.close_button.setFixedSize(12, 12)
        # self.close_button.setStyleSheet("border: none; background: none; color: #D73F3F;")

        self.menuButton = BurgerButton(self)
        self.menuButton.setFixedSize(18,13)
        # self.menuButton.move(0,self.width()-10)

        layout.addWidget(self.close_button)
        layout.addSpacing(10)  # Space after buttons

        # Add stretch to push search bar to the center
        layout.addStretch()

        # Search bar
        self.title = QLabel(self)
        self.title.setText("WiiiD")
        self.title.setStyleSheet("color: #959595; font: Menlo;")
        layout.addWidget(self.title)

        # Add stretch again to center it properly
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


class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove default title bar
        self.setAttribute(Qt.WA_TranslucentBackground)  # Enable transparency for rounded corners
        self.setGeometry(100, 100, 1200, 800)

        # Custom title bar
        self.title_bar = CustomTitleBar(self)
        self.setContentsMargins(0,0,0,0)

        # Main content area
        main_content = QWidget()
        main_content.setStyleSheet("background-color: rgba(255, 255, 255, 255); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;")

        # Apply macOS-style shadow
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

        self.setCentralWidget(container)


app = QApplication([])
window = CustomWindow()
window.show()
app.exec()
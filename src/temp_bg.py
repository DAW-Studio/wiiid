from PySide6.QtWidgets import QApplication

from quilt.widget import MainCustomWindow


if __name__ == "__main__":
    app = QApplication()

    window = MainCustomWindow()
    app.setStyleSheet("background-color: white")
    window.show()

    app.exec()
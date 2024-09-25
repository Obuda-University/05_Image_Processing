from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout


class PhotoshopApplication:
    def __init__(self) -> None:
        self.WINDOW_WIDTH: int = 300
        self.WINDOW_HEIGHT: int = 300
        self.WINDOW_TITLE: str = "Photoshop App"

    def create_application(self) -> (QApplication, QWidget):
        app = QApplication([])
        main_window = QWidget()
        main_window.setWindowTitle(self.WINDOW_TITLE)
        main_window.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        return app, main_window

    def run_application(self) -> None:
        app, main_window = self.create_application()
        main_window.show()
        app.exec()


if __name__ == '__main__':
    APP = PhotoshopApplication()
    APP.run_application()

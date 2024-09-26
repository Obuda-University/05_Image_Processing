from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu, QWidget, QLabel, QPushButton, QVBoxLayout
from CustomToolBar import CustomToolBar


class PhotoshopApplication(QMainWindow):
    def __init__(self) -> None:
        super(PhotoshopApplication, self).__init__()
        self.WINDOW_WIDTH: int = 1000
        self.WINDOW_HEIGHT: int = 800
        self.WINDOW_TITLE: str = "Photoshop App"
        self.WINDOW_ICON: str = "Resources\\icon2.png"

        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setWindowIcon(QIcon(self.WINDOW_ICON))

        self.create_toolbar()

    def create_toolbar(self) -> None:
        main_toolbar = CustomToolBar(self)
        self.addToolBar(main_toolbar)

        """new_action.triggered.connect(self.new_file)
        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)
        file_menu_action.triggered.connect(self.action)"""

    def action(self) -> None:
        print("asd")

    def new_file(self) -> None:
        print("NEW file action triggered")

    def open_file(self) -> None:
        print("OPEN file action triggered")

    def save_file(self) -> None:
        print("SAVE file action triggered")


def run_application() -> None:
    app = QApplication([])
    main_window = PhotoshopApplication()
    main_window.show()
    app.exec()


if __name__ == '__main__':
    run_application()

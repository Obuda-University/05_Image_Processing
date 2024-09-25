from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu, QToolBar, QWidget, QLabel, QPushButton, QVBoxLayout


class PhotoshopApplication(QMainWindow):
    def __init__(self) -> None:
        super(PhotoshopApplication, self).__init__()
        self.WINDOW_WIDTH: int = 1000
        self.WINDOW_HEIGHT: int = 800
        self.WINDOW_TITLE: str = "Photoshop App"

        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        self.create_toolbar()

    def create_toolbar(self) -> None:
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        menu = QMenu("File Actions", self)
        label = QLabel("Label", self)
        toolbar.addWidget(label)
        file_menu_action = QAction("File Actions", self)
        file_menu_action.setMenu(menu)
        toolbar.addAction(file_menu_action)

        new_action = QAction("New", self)
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)

        menu.addAction(new_action)
        menu.addAction(open_action)
        toolbar.addAction(save_action)

        new_action.triggered.connect(self.new_file)
        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)
        file_menu_action.triggered.connect(self.action)

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

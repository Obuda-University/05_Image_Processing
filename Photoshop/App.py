import sys
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QMenu


class Application(QMainWindow):
    def __init__(self) -> None:
        super(Application, self).__init__()
        self.title = "Photoshop Application"
        self.setWindowTitle(self.title)

        label = QLabel(self)
        pixmap = QPixmap("Resources/icon.png")
        label.setPixmap(pixmap)
        self.setCentralWidget(label)
        self.resize(pixmap.width(), pixmap.height())

        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        edit_menu = menubar.addMenu("&Edit")
        # TODO: Add extra icon for saving the file
        # TODO: Add extra icon for undoing (<-)
        # TODO: Add extra icon for redoing (->)
        # TODO: Add checkbox to disable toolbar

        # Actions for the file menu
        file_menu_actions: list[[(str, [str, None], str), None]] = [
            ("New", "Ctrl+N", self.new),
            ("Open", "Ctrl+O", self.open),
            None,
            ("Save", "Ctrl+S", self.save),
            ("Save as", None, self.save_as),
            None,
            ("Exit", None, self.exit),
        ]

        # Actions for the edit menu
        edit_menu_actions: list[[(str, [str, None], str), None]] = [
            ("Cut", "Ctrl+X", self.cut),
            ("Copy", "Ctrl+C", self.copy),
            ("Paste", "Ctrl+V", self.paste),
        ]

        self.create_menu_items(file_menu, file_menu_actions)
        self.create_menu_items(edit_menu, edit_menu_actions)

    def create_menu_items(self, menu: QMenu, action_list: list[[(str, [str, None], str), None]]) -> None:
        """Helper function to add functions to a menu"""
        for i in action_list:
            if i is None:
                menu.addSeparator()
            else:
                text, shortcut, callback = i
                act = QAction(text, self)
                if shortcut:
                    act.setShortcut(shortcut)
                act.triggered.connect(callback)
                menu.addAction(act)

    def new(self) -> None:
        print("New File Created!")

    def open(self) -> None:
        print("File Opened!")

    def save(self) -> None:
        print("File Saved!")

    def save_as(self) -> None:
        print("File Saved As!")

    def exit(self) -> None:
        print("Exited Application!")

    def cut(self) -> None:
        print("File Cut!")

    def copy(self) -> None:
        print("File Copied!")

    def paste(self) -> None:
        print("File Pasted!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Application()
    w.show()
    sys.exit(app.exec())

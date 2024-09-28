import sys
from Qt import QtCore
from CustomView import CustomView
from PyQt6.QtGui import QPixmap, QAction, QIcon, QWheelEvent
from PyQt6.QtWidgets import QMainWindow, QApplication, QMenu, QMenuBar, QLabel, QComboBox, QGraphicsScene


class Application(QMainWindow):
    def __init__(self) -> None:
        super(Application, self).__init__()
        self.setWindowTitle("Photoshop Application")
        self.setWindowIcon(QIcon("Resources/icon.png"))

        # Create the graphic scene
        self.scene = QGraphicsScene(self)
        self.view = CustomView(self.scene, self)
        self.setCentralWidget(self.view)

        # Load the image and add it to the scene
        self.image = QPixmap("Resources/icon.png")
        self.scene.addPixmap(self.image)
        self.view.setScene(self.scene)
        self.view.setSceneRect(self.image.rect().adjusted(0, 0, 0, 0).toRectF())

        main_menubar = self.menuBar()
        file_menu = main_menubar.addMenu("&File")
        edit_menu = main_menubar.addMenu("&Edit")

        # Actions for the main menu
        main_menu_actions: list[[(str, [str, None], str), None]] = [
            (QIcon.fromTheme("document-save"), None, self.save),
            (QIcon.fromTheme("edit-undo"), None, self.undo),
            (QIcon.fromTheme("edit-redo"), None, self.redo),
        ]

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
        self.create_menu_items(main_menubar, main_menu_actions)


        # TODO: Add toolbar items (transformation, grayscale, other functionalities)
        # TODO: Add Zoom functionality: selectable options with dropdown, but also editable with a number
        # TODO: Add Zoom functionality: Ctrl + ScrollWheel Up / Down

    def create_menu_items(self, menu: [QMenu, QMenuBar], action_list: list[[(str, [str, None], str), None]]) -> None:
        """Helper function to add functions to a menu"""
        for i in action_list:
            if i is None:
                menu.addSeparator()
            else:
                text, shortcut, callback = i
                if isinstance(text, str) and text != "":
                    act = QAction(text, self)
                    if shortcut:
                        act.setShortcut(shortcut)
                else:
                    act = QAction(text, "", self)
                act.triggered.connect(callback)
                menu.addAction(act)

    # TODO: Make functions
    def on_zoom_changed(self, text: str) -> None:
        zoom_factor = int(text.strip('%')) / 100.0
        self.view.set_zoom(zoom_factor)

    def undo(self) -> None:
        print("Undo!")

    def redo(self) -> None:
        print("Redo!")

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

    def grayscale(self) -> None:
        pass

    def rotate(self) -> None:
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Application()
    w.show()
    sys.exit(app.exec())

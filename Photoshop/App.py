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

        # Connect to the zoom_changed signal
        self.view.zoom_changed.connect(self.update_zoom_combobox)

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

        main_toolbar = self.addToolBar("Main Toolbar")

        zoom_label = QLabel("Zoom:")
        main_toolbar.addWidget(zoom_label)

        self.zoom_combobox = QComboBox()
        self.zoom_combobox.setFixedWidth(70)
        self.zoom_combobox.setEditable(True)
        self.zoom_combobox.addItems(["50%", "75%", "100%", "200%", "300%", "400%", "500%", "600%", "700%", "800%"])
        self.zoom_combobox.setCurrentText("100%")
        self.zoom_combobox.currentTextChanged.connect(self.on_zoom_changed)
        main_toolbar.addWidget(self.zoom_combobox)

        grayscale_action = QAction("Grayscale", self)
        main_toolbar.addAction(grayscale_action)
        grayscale_action.triggered.connect(self.grayscale)

        rotate_action = QAction("Rotate", self)
        main_toolbar.addAction(rotate_action)
        rotate_action.triggered.connect(self.rotate)

        self.setMouseTracking(True)

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
        try:
            zoom_value = int(text.strip('%'))
            if 10 > zoom_value > 800:
                raise ValueError
            self.view.set_zoom(zoom_value / 100.0)
        except ValueError:
            self.zoom_combobox.setCurrentText("100%")

    def update_zoom_combobox(self, zoom_factor: float) -> None:
        """Update the zoom combobox based on the zoom_factor from the CustomView"""
        zoom_percentage = int(zoom_factor * 100)
        self.zoom_combobox.setCurrentText(f"{zoom_percentage}%")

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

import sys
from CustomView import CustomView
from PyQt6.QtGui import QPixmap, QAction, QIcon, QUndoStack
from PyQt6.QtWidgets import (QMainWindow, QApplication, QMenu, QMenuBar, QToolBar, QLabel,
                             QComboBox, QGraphicsScene, QToolButton, QMessageBox)


class Application(QMainWindow):
    def __init__(self) -> None:
        super(Application, self).__init__()
        self.setWindowTitle("Photoshop Application")
        self.setWindowIcon(QIcon("Resources/icon.png"))

        # Create the graphic scene
        self.scene = QGraphicsScene(self)
        self.view = CustomView(self.scene, self)
        self.setCentralWidget(self.view)

        # Functionalities
        self.undo_stack = QUndoStack(self)
        self.clipboard = QApplication.clipboard()

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

        # Create toolbar actions
        self.toolbar_menus: dict = {}

        self.create_toolbar_action_items(main_toolbar, "Rotate", "Rotate Right 90°", self.rotate_right)
        self.create_toolbar_action_items(main_toolbar, "Rotate", "Rotate Right 90°", self.rotate_left)
        self.create_toolbar_action_items(main_toolbar, None, "Negate", self.negate)
        self.create_toolbar_action_items(main_toolbar, None, "Grayscale", self.grayscale)
        self.create_toolbar_action_items(main_toolbar, "Transformations", "Gamma Transformation", self.trans_gamma)
        self.create_toolbar_action_items(main_toolbar, "Transformations", "Logarithmic Transformation", self.trans_log)
        self.create_toolbar_action_items(main_toolbar, "Histograms", "Create Histogram", self.hist_create)
        self.create_toolbar_action_items(main_toolbar, "Histograms", "Equalize Histogram", self.hist_eq)
        self.create_toolbar_action_items(main_toolbar, "Filters", "Box Filter", self.filter_box)
        self.create_toolbar_action_items(main_toolbar, "Filters", "Gauss Filter", self.filter_gauss)
        self.create_toolbar_action_items(main_toolbar, "Edge Detections", "Sobel Edge Detection", self.edge_sobel)
        self.create_toolbar_action_items(main_toolbar, "Edge Detections", "Laplace Edge Detection", self.edge_laplace)
        self.create_toolbar_action_items(main_toolbar, None, "Characteristic Point Detection", self.point)

        self.setMouseTracking(True)

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

    def create_toolbar_action_items(self, toolbar: QToolBar, menu_name: [str, None],
                                    action_name: str, action: callable) -> None:
        """Helper function to add buttons to the toolbar and create menus"""
        q_action = QAction(action_name, self)
        q_action.triggered.connect(action)

        if not menu_name:
            toolbar.addAction(q_action)
        else:
            if menu_name in self.toolbar_menus:
                menu_button = self.toolbar_menus[menu_name]
                menu_button.menu().addAction(q_action)
            else:
                menu = QMenu()
                menu.addAction(q_action)

                menu_button = QToolButton()
                menu_button.setText(menu_name)
                menu_button.setMenu(menu)
                menu_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

                toolbar.addWidget(menu_button)
                self.toolbar_menus[menu_name] = menu_button

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

# region MenuBar Buttons
    def undo(self) -> None:
        print("Undo!")

    def redo(self) -> None:
        print("Redo!")

    def new(self) -> None:
        """Creates a new file by clearing the current scene"""
        reply = QMessageBox.question(self, 'Unsaved Work', "Do you want to save changes before creating a new file?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No |
                                     QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Yes:
            self.save()
        elif reply == QMessageBox.StandardButton.Cancel:
            return
        self.scene.clear()
        self.image = None

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
# endregion

# region ToolBar Buttons
    def negate(self) -> None:
        pass

    def grayscale(self) -> None:
        pass

    def trans_gamma(self) -> None:
        pass

    def trans_log(self) -> None:
        pass

    def hist_create(self) -> None:
        pass

    def hist_eq(self) -> None:
        pass

    def filter_box(self) -> None:
        pass

    def filter_gauss(self) -> None:
        pass

    def edge_sobel(self) -> None:
        pass

    def edge_laplace(self) -> None:
        pass

    def point(self) -> None:
        pass

    def rotate_right(self) -> None:
        pass

    def rotate_left(self) -> None:
        pass
# endregion

    def holder(self) -> None:
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Application()
    w.show()
    sys.exit(app.exec())

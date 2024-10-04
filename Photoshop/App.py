from PyQt6.QtWidgets import (QMainWindow, QApplication, QMenu, QMenuBar, QToolBar, QLabel, QGraphicsItem, QInputDialog,
                             QComboBox, QGraphicsScene, QToolButton, QMessageBox, QFileDialog, QGraphicsPixmapItem)
from PyQt6.QtGui import QPixmap, QAction, QIcon, QUndoStack
from ImageTransformations import ImageTransformations
from PyQt6.QtCore import Qt, QPointF
from CustomView import CustomView
import sys


class Application(QMainWindow):
    def __init__(self) -> None:
        self.WINDOW_WIDTH: int = 1000
        self.WINDOW_HEIGHT: int = 700
        self.image: [QPixmap, None] = None
        self.toolbar_menus: dict = {}
        self.current_file = None
        self.image_transformations = ImageTransformations()

        super(Application, self).__init__()
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setWindowTitle("Photoshop Application")
        self.setWindowIcon(QIcon("Resources/icon.png"))

        # Create the graphic scene
        self.scene = QGraphicsScene(self)
        self.view = CustomView(self.scene, self)
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

        # Functionalities
        self.undo_stack = QUndoStack(self)
        self.clipboard = QApplication.clipboard()

        # Connect to the zoom_changed signal
        self.view.zoom_changed.connect(self.update_zoom_combobox)

        main_menubar = self.menuBar()
        file_menu = main_menubar.addMenu("&File")
        edit_menu = main_menubar.addMenu("&Edit")

        # Add label to display the measured time
        self.time_label = QLabel(f"Time: 0.0s\t\t")
        main_menubar.setCornerWidget(self.time_label, Qt.Corner.TopRightCorner)

        # Actions for the main menu
        main_menu_actions: list[[(str, [str, None], str), None]] = [
            (QIcon.fromTheme("document-save"), None, self.save),
            (QIcon.fromTheme("edit-undo"), "Ctrl+Z", self.undo),
            (QIcon.fromTheme("edit-redo"), "Ctrl+Y", self.redo),
            ("Send to Back", None, self.send_image_back),
            ("Send to Front", None, self.send_image_front),
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
        self.create_toolbar_action_items(main_toolbar, "Rotate", "Rotate Right 90°", self.rotate_right)
        self.create_toolbar_action_items(main_toolbar, "Rotate", "Rotate Left 90°", self.rotate_left)
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
        self.create_toolbar_action_items(main_toolbar, None, "Point Detection", self.point)

        self.setMouseTracking(True)

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

    def dialog_no_selection(self, selected_items: [list[QGraphicsItem], list], text: str) -> None:
        if not selected_items:
            QMessageBox.information(self, "No Selection", text)
            return

    def dialog_question(self, window_name: str, text: str) -> QMessageBox.StandardButton:
        reply = QMessageBox.question(self, window_name, text, QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
        return reply

# region MenuBar Buttons
    # TODO: add actions to the todo stack
    def send_image_back(self) -> None:
        """Send the selected image behind all other images"""
        selected_items = self.scene.selectedItems()
        if selected_items:
            min_z_value = min([i.zValue() for i in self.scene.items()]) if self.scene.items() else 0
            for i, item in enumerate(selected_items):
                item.setZValue(min_z_value - (i + 1))

    def send_image_front(self) -> None:
        """Send the selected image in front of all other images"""
        selected_items = self.scene.selectedItems()
        if selected_items:
            max_z_value = max([i.zValue() for i in self.scene.items()]) if self.scene.items() else 0
            for i, item in enumerate(selected_items):
                item.setZValue(max_z_value + (i + 1))

    def undo(self) -> None:
        self.undo_stack.undo()
        print("undo")

    def redo(self) -> None:
        self.undo_stack.redo()
        print("redo")

    def new(self) -> None:
        """Creates a new file by clearing the current scene"""
        reply = self.dialog_question("Unsaved Work", "Do you want to save changes before creating a new file?")
        if reply == QMessageBox.StandardButton.Yes:
            self.save()
        elif reply == QMessageBox.StandardButton.Cancel:
            return
        self.scene.clear()
        self.image = None

    def open(self) -> None:
        """Opens an image file and loads it into the scene"""
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if filename:
            self.image = QPixmap(filename)
            # self.scene.clear()
            self.create_selectable_image(self.image)
            self.view.setSceneRect(self.image.rect().adjusted(0, 0, 0, 0).toRectF())

    def save(self) -> None:
        """Saves the current file"""
        if not hasattr(self, 'current_file') or self.current_file is None:
            self.save_as()
        else:
            self.image.save(self.current_file)

    def save_as(self) -> None:
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image As", "", "Images (*.png *.jpg *.bmp)")
        if file_name:
            self.current_file = file_name
            self.save()
            print("saved")

    def exit(self) -> None:
        reply = self.dialog_question("Exit Application", "Do you want to save changes before exiting?")
        if reply == QMessageBox.StandardButton.Yes:
            self.save()
        elif reply == QMessageBox.StandardButton.Cancel:
            return
        QApplication.quit()

    def cut(self) -> None:
        """Cuts the selected item to the clipboard"""
        selected_items = self.scene.selectedItems()
        if selected_items:
            item = selected_items[0]
            self.clipboard.setPixmap(item.pixmap())
            self.scene.removeItem(item)

    def copy(self) -> None:
        """Copies the selected item."""
        selected_items = self.scene.selectedItems()
        if selected_items:
            item = selected_items[0]
            self.clipboard.setPixmap(item.pixmap())

    def paste(self) -> None:
        """Pastes the clipboard image content"""
        pixmap = self.clipboard.pixmap()
        if not pixmap.isNull():
            self.image = pixmap
            self.create_selectable_image(pixmap)
# endregion

# region ToolBar Buttons
    def negate(self) -> None:
        """Invert the colors of the selected image(s)"""
        selected_items = self.scene.selectedItems()
        self.dialog_no_selection(selected_items, "Please select an image to negate.")
        items = self.create_copy(selected_items)
        time = self.image_transformations.measure_time(self.image_transformations.negate, items)
        self.time_label.setText(f"Time: {time:.4f}s\t\t")

    def grayscale(self) -> None:
        """Convert the selected image(s) to grayscale"""
        selected_items = self.scene.selectedItems()
        self.dialog_no_selection(selected_items, "Please select an image to grayscale.")
        items = self.create_copy(selected_items)
        time = self.image_transformations.measure_time(self.image_transformations.grayscale, items)
        self.time_label.setText(f"Time: {time:.4f}s\t\t")

    def trans_gamma(self) -> None:
        """Apply gamma transformation on the selected image(s)"""
        gamma_value, ok = QInputDialog.getDouble(self, "Gamma Correction", "Enter gamma value (e.g., 2.2):", 1.0, 0.1,
                                                 10.0, 2)
        if not ok:
            return
        selected_items = self.scene.selectedItems()
        self.dialog_no_selection(selected_items, "Please select an image for gamma correction.")
        items = self.create_copy(selected_items)
        time = self.image_transformations.measure_time(self.image_transformations.gamma_transformation,
                                                       items, gamma_value=gamma_value)
        self.time_label.setText(f"Time: {time:.4f}s\t\t")

    def trans_log(self) -> None:
        """Apply logarithmic transformation on the selected image(s)"""
        selected_items = self.scene.selectedItems()
        self.dialog_no_selection(selected_items, "Please select an image for gamma logarithmic transformation.")
        items = self.create_copy(selected_items)
        time = self.image_transformations.measure_time(self.image_transformations.logarithmic_transformation,items)
        self.time_label.setText(f"Time: {time:.4f}s\t\t")

    def hist_create(self) -> None:
        """Create a histogram of the selected image(s)"""
        selected_items = self.scene.selectedItems()
        self.dialog_no_selection(selected_items, "Please select an image to create a histogram.")
        time = self.image_transformations.measure_time(self.image_transformations.histogram_create, selected_items)
        self.time_label.setText(f"Time: {time:.4f}s\t\t")

    def hist_eq(self) -> None:
        """Apply histogram equalization to the selected image(s)"""
        selected_items = self.scene.selectedItems()
        self.dialog_no_selection(selected_items, "Please select an image for histogram equalization.")
        items = self.create_copy(selected_items)
        time = self.image_transformations.measure_time(self.image_transformations.histogram_equalize, items)
        self.time_label.setText(f"Time: {time:.4f}s\t\t")

    def filter_box(self) -> None:
        """Apply a box filter (mean filter) on the selected image(s)"""
        selected_items = self.scene.selectedItems()
        self.dialog_no_selection(selected_items, "Please select an image for box filtering.")
        items = self.create_copy(selected_items)
        time = self.image_transformations.measure_time(self.image_transformations.filter_box, items)
        self.time_label.setText(f"Time: {time:.4f}s\t\t")

    def filter_gauss(self) -> None:
        """Apply Gaussian filter on the selected image(s)"""
        selected_items = self.scene.selectedItems()
        self.dialog_no_selection(selected_items, "Please select an image for Gaussian filtering.")
        items = self.create_copy(selected_items)
        time = self.image_transformations.measure_time(self.image_transformations.filter_gauss, items)
        self.time_label.setText(f"Time: {time:.4f}s\t\t")

    def edge_sobel(self) -> None:
        """Apply Sobel edge detection on the selected image(s)"""
        selected_items = self.scene.selectedItems()
        self.dialog_no_selection(selected_items, "Please select an image for Sobel edge detection.")
        items = self.create_copy(selected_items)
        time = self.image_transformations.measure_time(self.image_transformations.edge_sobel, items)
        self.time_label.setText(f"Time: {time:.4f}s\t\t")

    def edge_laplace(self) -> None:
        """Apply Laplacian edge detection on the selected image(s)"""
        selected_items = self.scene.selectedItems()
        self.dialog_no_selection(selected_items, "Please select an image to apply Laplacian edge detection.")
        items = self.create_copy(selected_items)
        time = self.image_transformations.measure_time(self.image_transformations.edge_laplace, items)
        self.time_label.setText(f"Time: {time:.4f}s\t\t")

    def point(self) -> None:
        """Detect characteristic corners using the Lucas-Kanade (Shi-Tomasi) Operator on the selected image(s)"""
        selected_items = self.scene.selectedItems()
        self.dialog_no_selection(selected_items, "Please select an image to apply characteristic point detection.")
        max_corners, ok = QInputDialog.getInt(self, "Maximum Corners to Detect", "Enter max value:",
                                              200, 10, 1000, 1)
        if not ok:
            return
        items = self.create_copy(selected_items)
        time = self.image_transformations.measure_time(self.image_transformations.corner_detection_kanade,
                                                       items, max_corners=max_corners)
        self.time_label.setText(f"Time: {time:.4f}s\t\t")

    def rotate_right(self) -> None:
        pass

    def rotate_left(self) -> None:
        pass
# endregion

    def create_menu_items(self, menu: [QMenu, QMenuBar], action_list: list[[(str, [str, None], str), None]]) -> None:
        """Helper function to add functions to a menu"""
        for i in action_list:
            if i is None:
                menu.addSeparator()
            else:
                text, shortcut, callback = i
                if isinstance(text, str) and text != "":
                    act = QAction(text, self)
                else:
                    act = QAction(text, "", self)
                if shortcut:
                    act.setShortcut(shortcut)
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

    def create_selectable_image(self, pixmap: QPixmap) -> None:
        pixmap_item = QGraphicsPixmapItem(pixmap)
        pixmap_item.setFlags(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable |
                             QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable)
        self.scene.addItem(pixmap_item)

    def create_copy(self, selected_items: list[QGraphicsItem]) -> list[QGraphicsPixmapItem]:
        """Copies the selected image(s), applies the desired transformation, and places them next to the original."""
        if not selected_items:
            return []

        copied_items = []

        for item in selected_items:
            original_pixmap = item.pixmap()
            copied_item = QGraphicsPixmapItem(original_pixmap)

            original_pos = item.pos()
            copied_item.setPos(QPointF(original_pos.x() + original_pixmap.width() + 20, original_pos.y()))

            copied_item.setFlags(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable |
                                 QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable)

            self.scene.addItem(copied_item)
            copied_items.append(copied_item)

        return copied_items


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Application()
    w.show()
    sys.exit(app.exec())

import copy
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QImage, QPixmap, QPainter, QShortcut, QKeySequence
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QMessageBox, QFileDialog, QGraphicsView, QScrollArea,
    QGraphicsScene, QGraphicsPixmapItem, QHBoxLayout, QSlider, QStyle
)
import cv2
# import numpy as np


class AppState:
    """To store the state of the application"""
    def __init__(self, app: "PhotoshopApplication") -> None:
        self.image = copy.deepcopy(app.image)
        self.radius = app.radius
        self.sample_radius = app.sample_radius
        self.opacity = app.opacity


class PhotoshopApplication(QMainWindow):
    def __init__(self) -> None:
        super(PhotoshopApplication, self).__init__()

        self.WINDOW_WIDTH: int = 1000
        self.WINDOW_HEIGHT: int = 800
        self.WINDOW_TITLE: str = "Photoshop App"
        self.WINDOW_ICON: str = "Resources\\icon2.png"

        self.image = None
        self.healing_brush_active = False
        self.radius = 15
        self.sample_radius = 5
        self.zoom_level = 0
        self.opacity = 0.2
        self.history = []

        self.space_pressed = False
        self.last_cursor_pos = None
        self.dragging = False

        # self.round_cursor = self.create_round_cursor(self.radius)
        self.initUI()

        self.image = None

    def initUI(self) -> None:
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setWindowIcon(QIcon(self.WINDOW_ICON))

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        # IMAGE VIEW
        self.image_view = QGraphicsView(self)
        self.image_view.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.image_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        # events
        # dragging
        self.image_view.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        # zooming settings
        self.image_view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.image_view.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.image_view.setStyleSheet("border: none;")
        self.image_view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.image_view)

        self.main_layout.addWidget(self.scroll_area)

        self.scene = QGraphicsScene()
        self.image_view.setScene(self.scene)

        self.image_item = QGraphicsPixmapItem()
        self.scene.addItem(self.image_item)

        # menu bar
        menuBar = self.menuBar()
        menuBar.setStyleSheet("font-size: 15px")

        fileMenu = menuBar.addMenu("&File")
        editMenu = menuBar.addMenu("&Edit")

        load_act = QAction("Load Image", self)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirHomeIcon)
        load_act.setIcon(icon)
        load_act.setStatusTip("Load an Image")
        load_act.triggered.connect(self.load_image)
        fileMenu.addAction(load_act)

        undo_act = QAction("Undo", self)
        undo_act.setStatusTip("Undo")
        undo_act.triggered.connect(self.load_last_state)
        editMenu.addAction(undo_act)

        save_act = QAction("Save", self)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton)
        save_act.setIcon(icon)
        save_act.triggered.connect(self.save_image)
        fileMenu.addAction(save_act)

    def is_inside_image(self, x, y):
        """Checks if pressed position is inside images bounds"""
        return 0 <= x < self.image.shape[1] and 0 <= y < self.image.shape[0]

    def load_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)"
        )
        if file_path:
            self.image = cv2.imread(file_path)
            self.update_image_label()
            self.image_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.save_state()

    def update_image_label(self):
        if self.image is not None:
            colored_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            qt_img = QImage(
                colored_img.data, colored_img.shape[1], colored_img.shape[0],
                colored_img.shape[1] * 3, QImage.Format.Format_RGB888
            )
            pixmap = QPixmap.fromImage(qt_img)
            self.image_item.setPixmap(pixmap)

    def load_last_state(self):
        if len(self.history) == 0:
            return

        state: AppState = self.history.pop()
        self.image = state.image
        self.radius = state.radius
        self.opacity = state.opacity
        self.sample_radius = state.sample_radius
        self.update_image_label()
        self.update()

    def save_state(self):
        state = AppState(self)
        self.history.append(state)

    def save_image(self):
        file, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file:
            cv2.imwrite(file, self.image)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = PhotoshopApplication()
    main_window.show()
    sys.exit(app.exec())

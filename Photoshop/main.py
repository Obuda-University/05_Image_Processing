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

        self.menubar = self.menuBar()

        # IMAGE VIEW
        self.image_view = QGraphicsView(self)
        self.image_view.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.image_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        # events
        self.image_view.mousePressEvent = self.mousePressEventIMG
        self.image_view.mouseMoveEvent = self.mouseMoveEventIMG
        self.image_view.mouseReleaseEvent = self.mouseReleaseEventIMG
        self.image_view.wheelEvent = self.wheelEventIMG
        # dragging
        self.image_view.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        # zooming settings
        self.image_view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.image_view.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        self.image_view.setStyleSheet("border: none;")
        self.image_view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        # self.image_view.setCursor(self.round_cursor)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.image_view)

        self.main_layout.addWidget(self.scroll_area)

        self.scene = QGraphicsScene()
        self.image_view.setScene(self.scene)

        self.image_item = QGraphicsPixmapItem()
        self.scene.addItem(self.image_item)

        self.radius_slider_layout = QHBoxLayout()
        self.radius_slider = QSlider(Qt.Orientation.Horizontal)
        self.radius_slider.setRange(1, 50)
        self.radius_slider.setValue(self.radius)
        self.radius_slider.valueChanged.connect(self.radiusChanged)

        self.radius_label = QLabel(f"Radius ({self.radius})")

        self.radius_slider_layout.addWidget(self.radius_label)
        self.radius_slider_layout.addWidget(self.radius_slider)

        self.sample_slider_layout = QHBoxLayout()
        self.sample_slider = QSlider(Qt.Orientation.Horizontal)
        self.sample_slider.setRange(1, 50)
        self.sample_slider.setValue(self.sample_radius)
        self.sample_slider.valueChanged.connect(self.sampleChanged)

        self.sample_label = QLabel(f"Sample Radius (Higher is slower) ({self.sample_radius})")

    def radiusChanged(self) -> None:
        pass

    def sampleChanged(self) -> None:
        pass

    def mousePressEventIMG(self, event) -> None:
        pass

    def mouseMoveEventIMG(self, event) -> None:
        pass

    def mouseReleaseEventIMG(self, event) -> None:
        pass

    def wheelEventIMG(self, evebt) -> None:
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = PhotoshopApplication()
    main_window.show()
    sys.exit(app.exec())

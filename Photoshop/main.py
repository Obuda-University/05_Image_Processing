from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu, QWidget, QLabel, QPushButton, QVBoxLayout
import cv2
import numpy as np


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

        self.create_menu()
        self.create_main_widget()

        self.image = None

    def create_menu(self) -> None:
        self.menubar = self.menuBar()

        # Define Menu Titles
        menu_transformations = self.menubar.addMenu("&Transformations")
        menu_histograms = self.menubar.addMenu("&Histograms")
        menu_filters = self.menubar.addMenu("&Filters")
        menu_edges = self.menubar.addMenu("&Edge Detections")
        menu_file = self.menubar.addMenu("&File Operations")

        # Create actions
        act_negate = QAction("Negate", self)
        act_grayscale = QAction("Grayscale", self)
        act_gamma_transform = QAction("Gamma Transformation", self)
        act_log_transform = QAction("Logarithmic Transformation", self)
        act_histogram_create = QAction("Create Histogram", self)
        act_histogram_equalization = QAction("Histogram Equalization", self)
        act_box_filter = QAction("Box Filter", self)
        act_gauss_filter = QAction("Gauss Filter", self)
        act_sobel_edge_detection = QAction("Sobel Edge Detection", self)
        act_laplace_edge_detection = QAction("Laplace Edge Detection", self)
        act_point_detection = QAction("Point Detection", self)
        act_open_file = QAction("Open File", self)
        act_reset_to_default = QAction("Reset to Default", self)
        act_save_file = QAction("Save", self)

        # Connect actions to functions
        act_open_file.triggered.connect(self.open_file)
        act_save_file.triggered.connect(self.save_file)
        act_negate.triggered.connect(self.negate_image)
        act_grayscale.triggered.connect(self.grayscale_image)

        # Add actions to menus
        menu_transformations.addAction(act_gamma_transform)
        menu_transformations.addAction(act_log_transform)
        menu_histograms.addAction(act_histogram_create)
        menu_histograms.addAction(act_histogram_equalization)
        menu_filters.addAction(act_box_filter)
        menu_filters.addAction(act_gauss_filter)
        menu_edges.addAction(act_sobel_edge_detection)
        menu_edges.addAction(act_laplace_edge_detection)
        menu_edges.addAction(act_point_detection)
        menu_file.addAction(act_open_file)
        menu_file.addAction(act_reset_to_default)
        menu_file.addAction(act_save_file)

    def create_main_widget(self) -> None:
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setText("Drag and drop an image here or use the 'Open File' menu")

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.main_widget.setLayout(layout)

        # Enable drag and drop
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.DropAction.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.load_image(file_path)
            event.accept()
        else:
            event.ignore()

    def open_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.load_image(file_path)

    def load_image(self, file_path: str) -> None:
        self.image = cv2.imread(file_path)
        if self.image is not None:
            self.display_image()
        else:
            QMessageBox.critical(self, "Error", "Unable to load the image.")

    def display_image(self) -> None:
        height, width = self.image.shape[:2]
        bytes_per_line = 3 * width
        q_image = QImage(self.image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                                 Qt.TransformationMode.SmoothTransformation))

    def save_file(self) -> None:
        if self.image is not None:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                       "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp)")
            if file_path:
                cv2.imwrite(file_path, self.image)
        else:
            QMessageBox.warning(self, "Warning", "No image to save.")

    def negate_image(self) -> None:
        if self.image is not None:
            self.image = cv2.bitwise_not(self.image)
            self.display_image()
        else:
            QMessageBox.warning(self, "Warning", "No image loaded.")

    def grayscale_image(self) -> None:
        if self.image is not None:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)  # Convert back to 3 channels
            self.display_image()
        else:
            QMessageBox.warning(self, "Warning", "No image loaded.")


def run_application() -> None:
    app = QApplication([])
    main_window = PhotoshopApplication()
    main_window.show()
    app.exec()


if __name__ == '__main__':
    run_application()

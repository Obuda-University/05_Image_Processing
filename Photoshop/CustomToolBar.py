from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QToolBar


class CustomToolBar(QToolBar):
    def __init__(self, parent: QMainWindow = None) -> None:
        super().__init__("Main Toolbar", parent)
        self.menu = parent.menuBar()
        self.create_tools()

    def create_tools(self) -> None:

        # Define Menu Titles
        menu_transformations = self.menu.addMenu("&Transformations")
        menu_histograms = self.menu.addMenu("&Histograms")
        menu_filters = self.menu.addMenu("&Filters")
        menu_edges = self.menu.addMenu("&Edge Detections")
        menu_file = self.menu.addMenu("&File Operations")

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

        """self.addAction(act_negate)
        self.addAction(act_gamma_transform)
        self.addAction(act_log_transform)
        self.addAction(act_grayscale)
        self.addAction(act_histogram_create)
        self.addAction(act_histogram_equalization)
        self.addAction(act_box_filter)
        self.addAction(act_gauss_filter)
        self.addAction(act_sobel_edge_detection)
        self.addAction(act_laplace_edge_detection)
        self.addAction(act_point_detection)
        self.addAction(act_open_file)
        self.addAction(act_reset_to_default)
        self.addAction(act_save_file)"""

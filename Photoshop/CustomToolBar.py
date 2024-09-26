from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QToolBar, QMenu


class CustomToolBar(QToolBar):
    def __init__(self, parent=None) -> None:
        super().__init__("Main Toolbar", parent)

        self.create_tools()

    def create_tools(self) -> None:
        """menu = QMenu("Main Menu", self)
        file_menu_action = QAction("", self)
        file_menu_action.setMenu(menu)
        self.addAction(file_menu_action)"""

        act_negate = QAction("Negate", self)
        act_gamma_transform = QAction("Gamma Transformation", self)
        act_log_transform = QAction("Logarithmic Transformation", self)
        act_grayscale = QAction("Grayscale", self)
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

        self.addAction(act_negate)
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
        self.addAction(act_save_file)

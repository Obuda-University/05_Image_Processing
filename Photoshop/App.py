import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Application()
    w.show()
    sys.exit(app.exec())

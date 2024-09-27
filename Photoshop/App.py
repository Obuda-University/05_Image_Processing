import sys
from PyQt6.QtGui import QPixmap, QAction
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

        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        edit_menu = menubar.addMenu("&Edit")
        # TODO: Add extra icon for saving the file
        # TODO: Add extra icon for undoing (<-)
        # TODO: Add extra icon for redoing (->)
        # TODO: Add checkbox to disable toolbar

        # Actions for the file menu
        act_file_new = QAction("New", self)  # Ctrl + N shortcut
        act_file_open = QAction("Open", self)  # Ctrl + O shortcut
        act_file_save = QAction("Save", self)  # Ctrl + S shortcut
        act_file_save_as = QAction("Save as", self)
        act_file_exit = QAction("Exit", self)

        file_menu.addAction(act_file_new)
        file_menu.addAction(act_file_open)
        file_menu.addSeparator()
        file_menu.addAction(act_file_save)
        file_menu.addAction(act_file_save_as)
        file_menu.addSeparator()
        file_menu.addAction(act_file_exit)

        # Actions for the edit menu
        act_edit_cut = QAction("Cut", self)  # Ctrl + X shortcut
        act_edit_copy = QAction("Copy", self)  # Ctrl + C shortcut
        act_edit_paste = QAction("Paste", self)  # Ctrl + V shortcut

        edit_menu.addAction(act_edit_cut)
        edit_menu.addAction(act_edit_copy)
        edit_menu.addAction(act_edit_paste)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Application()
    w.show()
    sys.exit(app.exec())

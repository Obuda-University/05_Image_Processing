from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtGui import QPainter, QWheelEvent


class CustomView(QGraphicsView):
    def __init__(self, *args, **kwargs) -> None:
        super(CustomView, self).__init__(*args, **kwargs)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.scale_factor = 1.0

    def wheelEvent(self, event: QWheelEvent) -> None:
        from PyQt6.QtCore import Qt
        """Handle zooming with Ctrl + ScrollWheel"""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:  # Scroll Up
                self.zoom_in()
            else:  # Scroll Down
                self.zoom_out()
        else:
            super(CustomView, self).wheelEvent(event)

    def zoom_in(self) -> None:
        """Scales the window up"""
        self.scale(1.1, 1.1)
        self.scale_factor *= 1.1

    def zoom_out(self) -> None:
        """Scales the window down"""
        self.scale(0.9, 0.9)
        self.scale_factor *= 0.9

    def set_zoom(self, factor: float) -> None:
        """Set the zoom with a specific factor"""
        self.resetTransform()
        self.scale(factor, factor)
        self.scale_factor = factor
    
from PyQt6.QtGui import QImage, QPixmap, QColor
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
import numpy as np


class ImageTransformations:
    def __init__(self) -> None:
        pass

    @staticmethod
    def negate(selected_items: [list[QGraphicsItem], list]) -> None:
        """Invert the colors of the selected image(s)"""
        for item in selected_items:
            if isinstance(item, QGraphicsPixmapItem):
                pixmap = item.pixmap()
                image = pixmap.toImage().convertToFormat(QImage.Format.Format_RGBA8888)
                width, height = image.width(), image.height()

                ptr = image.bits()
                ptr.setsize(image.sizeInBytes())

                arr = np.array(ptr).reshape((height, width, 4))  # RGBA format
                arr[..., :3] = 255 - arr[..., :3]  # Invert the RGB values excluding the alpha channel
                negated_image = QImage(arr.data, width, height, image.bytesPerLine(), image.format())
                negated_pixmap = QPixmap.fromImage(negated_image)
                item.setPixmap(negated_pixmap)

    @staticmethod
    def grayscale(selected_items: [list[QGraphicsItem], list]) -> None:
        for item in selected_items:
            if isinstance(item, QGraphicsPixmapItem):
                pixmap = item.pixmap()
                image = pixmap.toImage().convertToFormat(QImage.Format.Format_RGBA8888)

                width, height = image.width(), image.height()
                gray_image = QImage(width, height, image.format())

                for x in range(width):
                    for y in range(height):
                        color = image.pixelColor(x, y)
                        gray_value = int(0.299 * color.red() + 0.587 * color.green() + 0.144 * color.blue())
                        gray_color = QColor(gray_value, gray_value, gray_value, color.alpha())
                        gray_image.setPixelColor(x, y, gray_color)

                item.setPixmap(QPixmap.fromImage(gray_image))

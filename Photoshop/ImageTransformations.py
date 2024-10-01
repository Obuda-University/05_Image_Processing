from PyQt6.QtGui import QImage, QPixmap
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
                image = pixmap.toImage()
                image = image.convertToFormat(QImage.Format.Format_RGBA8888)
                width: int = image.width()
                height: int = image.height()

                ptr = image.bits()
                ptr.setsize(image.sizeInBytes())

                arr = np.array(ptr).reshape((height, width, 4))  # RGBA format
                arr[..., :3] = 255 - arr[..., :3]  # Invert the RGB values excluding the alpha channel
                negated_image = QImage(arr.data, width, height, image.bytesPerLine(), image.format())
                negated_pixmap = QPixmap.fromImage(negated_image)
                item.setPixmap(negated_pixmap)

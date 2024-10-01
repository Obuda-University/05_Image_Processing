from PyQt6.QtGui import QImage, QPixmap, QColor
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
import numpy as np
import matplotlib.pyplot as plt
import cv2


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
        """Convert the selected image(s) to grayscale"""
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

    @staticmethod
    def gamma_transformation(selected_items: [list[QGraphicsItem], list], gamma_value: float) -> None:
        """Apply gamma transformation on the selected image(s)"""
        for item in selected_items:
            if isinstance(item, QGraphicsPixmapItem):
                pixmap = item.pixmap()
                image = pixmap.toImage().convertToFormat(QImage.Format.Format_RGBA8888)

                width, height = image.width(), image.height()
                gamma_image = QImage(width, height, image.format())

                for x in range(width):
                    for y in range(height):
                        color = image.pixelColor(x, y)
                        r = int(255 * ((color.red() / 255) ** gamma_value))
                        g = int(255 * ((color.green() / 255) ** gamma_value))
                        b = int(255 * ((color.blue() / 255) ** gamma_value))
                        gamma_color = QColor(r, g, b, color.alpha())
                        gamma_image.setPixelColor(x, y, gamma_color)

                item.setPixmap(QPixmap.fromImage(gamma_image))

    @staticmethod
    def logarithmic_transformation(selected_items: [list[QGraphicsItem], list]) -> None:
        """Apply logarithmic transformation on the selected image(s)"""
        c: float = 255 / np.log(1 + 255)  # Scaling factor for logarithmic transformation

        for item in selected_items:
            if isinstance(item, QGraphicsPixmapItem):
                pixmap = item.pixmap()
                image = pixmap.toImage().convertToFormat(QImage.Format.Format_RGBA8888)

                width, height = image.width(), image.height()
                log_image = QImage(width, height, image.format())

                for x in range(width):
                    for y in range(height):
                        color = image.pixelColor(x, y)
                        r = int(c * np.log(1 + color.red()))
                        g = int(c * np.log(1 + color.green()))
                        b = int(c * np.log(1 + color.blue()))
                        log_color = QColor(r, g, b, color.alpha())
                        log_image.setPixelColor(x, y, log_color)

                item.setPixmap(QPixmap.fromImage(log_image))

    @staticmethod
    def histogram_create(selected_items: [list[QGraphicsItem], list]) -> None:
        """Create a histogram of the selected image(s)"""
        for item in selected_items:
            if isinstance(item, QGraphicsPixmapItem):
                pixmap = item.pixmap()
                image = pixmap.toImage()

                width, height = image.width(), image.height()
                pixel_data = np.zeros((height, width, 3), dtype=np.uint8)

                for x in range(width):
                    for y in range(height):
                        color = image.pixelColor(x, y)
                        pixel_data[y, x, 0] = color.red()
                        pixel_data[y, x, 1] = color.green()
                        pixel_data[y, x, 2] = color.blue()

                plt.hist(pixel_data.ravel(), bins=256, color='black', alpha=0.7, histtype='bar', density=True)
                plt.xlabel('Pixel Intensity')
                plt.ylabel('Frequency')
                plt.title('Histogram')
                plt.show()

    @staticmethod
    def histogram_equalize(selected_items: [list[QGraphicsItem], list]) -> None:
        """Apply histogram equalization to the selected image(s)"""
        for item in selected_items:
            if isinstance(item, QGraphicsPixmapItem):
                pixmap = item.pixmap()
                image = pixmap.toImage().convertToFormat(QImage.Format.Format_RGBA8888)

                width, height = image.width(), image.height()
                img_data = np.zeros((height, width, 3), dtype=np.uint8)

                for x in range(width):
                    for y in range(height):
                        color = image.pixelColor(x, y)
                        img_data[y, x] = [color.red(), color.green(), color.blue()]

                img_eq = np.zeros_like(img_data)
                for i in range(3):
                    img_eq[..., i] = cv2.equalizeHist(img_data[..., i])

                eq_image = QImage(img_eq.data, width, height, image.bytesPerLine(), image.format())
                item.setPixmap(QPixmap.fromImage(eq_image))

    @staticmethod
    def filter_box(selected_items: [list[QGraphicsItem], list]) -> None:
        """Apply a box filter (mean filter) on the selected image(s)"""
        for item in selected_items:
            if isinstance(item, QGraphicsPixmapItem):
                pixmap = item.pixmap()
                image = pixmap.toImage().convertToFormat(QImage.Format.Format_RGBA8888)

                width, height = image.width(), image.height()
                img_data = np.zeros((height, width, 3), dtype=np.uint8)

                for x in range(width):
                    for y in range(height):
                        color = image.pixelColor(x, y)
                        img_data[y, x] = [color.red(), color.green(), color.blue()]

                filtered_data = cv2.blur(img_data, (5, 5))
                filtered_image = QImage(filtered_data.data, width, height, image.bytesPerLine(), image.format())
                item.setPixmap(QPixmap.fromImage(filtered_image))


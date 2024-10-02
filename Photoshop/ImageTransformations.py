from PyQt6.QtWidgets import QGraphicsItem, QGraphicsPixmapItem
from PyQt6.QtGui import QImage, QPixmap, QColor
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import numpy as np
import cv2


# TODO: the original image should stay and the transformed image should be next to it
# TODO: show runtime of the function
class ImageTransformations:
    def __init__(self) -> None:
        pass

    @staticmethod
    def _q_image_to_np(image: QImage) -> np.ndarray:
        """Helper function to convert QImage to a NumPy array"""
        image = image.convertToFormat(QImage.Format.Format_RGBA8888)
        width, height = image.width(), image.height()
        ptr = image.bits()
        ptr.setsize(image.sizeInBytes())
        return np.array(ptr).reshape((height, width, 4)).copy()  # Deep copy to ensure memory is properly managed

    @staticmethod
    def _np_to_q_image(arr: np.ndarray, image_format: QImage.Format) -> QImage:
        """Helper function to convert NumPy array back to QImage"""
        height, width, _ = arr.shape
        return QImage(arr.data, width, height, image_format).copy()  # Ensure to not reference unsafe memory

    def negate(self, selected_items: list[QGraphicsItem]) -> None:
        """Invert the colors of the selected image(s)"""
        for item in selected_items:
            pixmap = item.pixmap()
            if pixmap.isNull():
                continue
            image = pixmap.toImage()
            img_array = self._q_image_to_np(image)
            img_array[..., :3] = 255 - img_array[..., :3]
            negated_image = self._np_to_q_image(img_array, image.format())
            item.setPixmap(QPixmap.fromImage(negated_image))

    def grayscale(self, selected_items: list[QGraphicsItem]) -> None:
        """Convert the selected image(s) to grayscale"""
        for item in selected_items:
            pixmap = item.pixmap()
            image = pixmap.toImage()
            img_array = self._q_image_to_np(image)
            grayscale_values = np.dot(img_array[..., :3], [0.299, 0.587, 0.114])
            img_array[..., :3] = grayscale_values[..., None]
            gray_image = self._np_to_q_image(img_array, image.format())
            item.setPixmap(QPixmap.fromImage(gray_image))

    def gamma_transformation(self, selected_items: list[QGraphicsItem], gamma_value: float) -> None:
        """Apply gamma transformation on the selected image(s)"""
        inv_gamma = 1.0 / gamma_value
        for item in selected_items:
            pixmap = item.pixmap()
            image = pixmap.toImage()
            img_array = self._q_image_to_np(image)
            img_array[..., :3] = (255 * ((img_array[..., :3] / 255) ** inv_gamma)).clip(0, 255).astype(np.uint8)
            gamma_image = self._np_to_q_image(img_array, image.format())
            item.setPixmap(QPixmap.fromImage(gamma_image))

    def logarithmic_transformation(self, selected_items: list[QGraphicsItem]) -> None:
        """Apply logarithmic transformation on the selected image(s)"""
        c: float = 255 / np.log(1 + 255)  # Scaling factor for logarithmic transformation
        for item in selected_items:
            pixmap = item.pixmap()
            image = pixmap.toImage()
            img_array = self._q_image_to_np(image)
            img_array[..., :3] = (c * np.log(1 + img_array[..., :3])).clip(0, 255).astype(np.uint8)
            log_image = self._np_to_q_image(img_array, image.format())
            item.setPixmap(QPixmap.fromImage(log_image))

    def histogram_create(self, selected_items: list[QGraphicsItem]) -> None:
        """Create a histogram of the selected image(s)"""
        for item in selected_items:
            pixmap = item.pixmap()
            image = pixmap.toImage()
            img_array = self._q_image_to_np(image)
            plt.hist(img_array[..., :3].ravel(), bins=256, color='black', alpha=0.7, histtype='bar', density=True)
            plt.xlabel('Pixel Intensity')
            plt.ylabel('Frequency')
            plt.title('Histogram')
            plt.show()

    def histogram_equalize(self, selected_items: list[QGraphicsItem]) -> None:
        """Apply histogram equalization to the selected image(s)"""
        for item in selected_items:
            pixmap = item.pixmap()
            image = pixmap.toImage()
            img_array = self._q_image_to_np(image)
            for i in range(3):  # Apply equalization on R, G, B channels
                img_array[..., i] = cv2.equalizeHist(img_array[..., i])
            eq_image = self._np_to_q_image(img_array, image.format())
            item.setPixmap(QPixmap.fromImage(eq_image))

    def filter_box(self, selected_items: list[QGraphicsItem]) -> None:
        """Apply a box filter (mean filter) on the selected image(s)"""
        for item in selected_items:
            pixmap = item.pixmap()
            image = pixmap.toImage()
            img_array = self._q_image_to_np(image)
            img_array[..., :3] = cv2.blur(img_array[..., :3], (5, 5))
            filtered_image = self._np_to_q_image(img_array, image.format())
            item.setPixmap(QPixmap.fromImage(filtered_image))

    def filter_gauss(self, selected_items: list[QGraphicsItem]) -> None:
        """Apply Gaussian filter on the selected image(s)"""
        for item in selected_items:
            pixmap = item.pixmap()
            image = pixmap.toImage()
            img_array = self._q_image_to_np(image)
            img_array[..., :3] = gaussian_filter(img_array[..., :3], sigma=2)
            gauss_image = self._np_to_q_image(img_array, image.format())
            item.setPixmap(QPixmap.fromImage(gauss_image))

    def edge_sobel(self, selected_items: list[QGraphicsItem]) -> None:
        """Apply Sobel edge detection on the selected image(s)"""
        for item in selected_items:
            pixmap = item.pixmap()
            if pixmap.isNull():
                continue
            image = pixmap.toImage()
            img_array = self._q_image_to_np(image)
            gray = cv2.cvtColor(img_array[..., :3], cv2.COLOR_RGBA2GRAY)

            sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            sobel = np.hypot(sobel_x, sobel_y).clip(0, 255).astype(np.uint8)

            # Add the detected edges as an overlay on the original image
            img_array[..., :3] = cv2.cvtColor(sobel, cv2.COLOR_GRAY2RGBA)[..., :3]
            sobel_image = self._np_to_q_image(img_array, image.format())
            item.setPixmap(QPixmap.fromImage(sobel_image))

    @staticmethod
    def edge_laplace(selected_items: list[QGraphicsItem]) -> None:
        """Apply Laplacian edge detection to the selected image(s)"""
        for item in selected_items:
            if isinstance(item, QGraphicsPixmapItem):
                pixmap = item.pixmap()
                image = pixmap.toImage().convertToFormat(QImage.Format.Format_RGBA8888)
                width, height = image.width(), image.height()

                laplacian_image = QImage(width, height, QImage.Format.Format_RGBA8888)
                laplacian_kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])

                for x in range(1, width - 1):
                    for y in range(1, height - 1):
                        r = g = b = 0
                        for i in range(3):
                            for j in range(3):
                                color = image.pixelColor(x - 1 + i, y - 1 + j)
                                r += color.red() * laplacian_kernel[i, j]
                                g += color.green() * laplacian_kernel[i, j]
                                b += color.blue() * laplacian_kernel[i, j]

                        laplace_color = QColor(min(max(r + 128, 0), 255),
                                               min(max(g + 128, 0), 255),
                                               min(max(b + 128, 0), 255),
                                               255)
                        laplacian_image.setPixelColor(x, y, laplace_color)

                negated_pixmap = QPixmap.fromImage(laplacian_image)
                item.setPixmap(negated_pixmap)

    def edge_laplace_optimized(self, selected_items: list[QGraphicsItem]) -> None:
        for item in selected_items:
            pixmap = item.pixmap()
            if pixmap.isNull():
                continue

            image = pixmap.toImage()
            img_array = self._q_image_to_np(image)

            # Convert to grayscale for edge detection
            gray = cv2.cvtColor(img_array[..., :3], cv2.COLOR_RGBA2GRAY)

            # Apply the Laplacian operator using OpenCV
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            laplacian = np.abs(laplacian).clip(0, 255).astype(np.uint8)  # Take absolute value and ensure it's in range

            # Convert back to RGBA format to overlay on original image
            img_array[..., :3] = cv2.cvtColor(laplacian, cv2.COLOR_GRAY2RGBA)[..., :3]

            # Convert the result back to QImage and set on the item
            laplace_image = self._np_to_q_image(img_array, image.format())
            item.setPixmap(QPixmap.fromImage(laplace_image))

    def corner_detection_kandae(self, selected_items: list[QGraphicsItem], max_corners: int = 400,
                                quality_level: float = 0.01, min_distance: int = 10) -> None:
        """Detect characteristic corners using the Lucas-Kanade (Shi-Tomasi) Operator on the selected image(s)"""
        for item in selected_items:
            pixmap = item.pixmap()
            if pixmap.isNull():
                continue

            image = pixmap.toImage()
            img_array = self._q_image_to_np(image)
            gray = cv2.cvtColor(img_array[..., :3], cv2.COLOR_RGBA2GRAY)

            # Use Shi-Tomasi corner detection (goodFeaturesToTrack)
            corners = cv2.goodFeaturesToTrack(gray, maxCorners=max_corners,
                                              qualityLevel=quality_level, minDistance=min_distance)
            if corners is not None:
                corners = np.int0(corners)
                for corner in corners:
                    x, y = corner.ravel()
                    cv2.circle(img_array, (x, y), 5, (255, 0, 0, 255), 1)  # Draw red circles for corners

            final_image = self._np_to_q_image(img_array, image.format())
            item.setPixmap(QPixmap.fromImage(final_image))

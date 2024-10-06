import cv2
import numpy as np
import matplotlib.pyplot as plt

# region Task 1
image = np.array([[0, 1, 5, 5, 5, 5, 5, 0],
                  [1, 1, 1, 4, 5, 5, 5, 4],
                  [1, 0, 0, 1, 6, 6, 6, 4],
                  [1, 0, 0, 3, 6, 6, 6, 4],
                  [1, 0, 3, 3, 6, 4, 4, 7],
                  [0, 0, 3, 2, 6, 4, 4, 4],
                  [0, 2, 2, 2, 6, 4, 4, 4],
                  [0, 2, 2, 2, 4, 6, 4, 0]], dtype=np.uint8)

# Draw Histogram:
hist, bins = np.histogram(image.flatten(), bins=8, range=(0, 8))

# Apply histogram equalization
image_equalized = cv2.equalizeHist(image)

plt.figure(figsize=(12, 6))
# Plot original
plt.subplot(1, 2, 1)
plt.bar(bins[:-1], hist, width=0.7, color='gray', align='center')
plt.title('Original Histogram')
plt.xlabel('Intensity Value')
plt.ylabel('Frequency')
# Plot equalized
plt.subplot(1, 2, 2)
plt.imshow(image_equalized, cmap='gray')
plt.title('Transformed Image')
plt.colorbar()

plt.tight_layout()
plt.show()
# endregion

# region Task 2
binary_image = np.zeros((10, 10), dtype=np.uint8)
binary_image[3:7, 3:7] = 1

# Apply Sobel Operator
sobel_x = cv2.Sobel(binary_image, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(binary_image, cv2.CV_64F, 0, 1, ksize=3)

# Gradient magnitude and direction
gradient_magnitude = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
gradient_direction = np.arctan2(sobel_y, sobel_x) * (180 / np.pi)

# Show Results
plt.subplot(1, 3, 1)
plt.imshow(binary_image, cmap='gray')
plt.title('Binary Image')
plt.colorbar()

plt.subplot(1, 3, 2)
plt.imshow(gradient_direction, cmap='hsv')
plt.title('Gradient Direction')
plt.colorbar()

plt.subplot(1, 3, 3)
plt.imshow(gradient_magnitude, cmap='gray')
plt.title('Gradient Magnitude')
plt.colorbar()

plt.show()
# endregion

# region Task 3

# endregion



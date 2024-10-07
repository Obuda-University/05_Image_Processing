from Assignment.HandTracking import HandTracking
from pynput.keyboard import Controller, Key
import numpy as np
import threading
import cv2

# TODO: backspace needed for the keyboard
# TODO: Shift for the keyboard


class OnScreenKeyboard:
    def __init__(self) -> None:
        self.keys: list[[Key, str]] = ['Q', Key.space]
        self.key_width, self.key_height = 100, 100
        self.start_x, self.start_y = 50, 50
        self.keyboard_image = np.zeros((600, 800, 3), dtype=np.uint8)

    def _draw_keyboard(self, frame: np.ndarray) -> None:
        for i, row in enumerate(self.keys):
            for j, key in enumerate(row):
                x = self.start_x + j * self.key_width
                y = self.start_y + i * self.key_height

                # Draw a rectangle for the key
                cv2.rectangle(self.keyboard_image, (x, y), (x + self.key_width, y + self.key_height), (255, 255, 255),
                              2)

                # Determine the label for the key
                label = str(key).replace("Key.", "")  # Remove 'Key.' from special keys for display

                # Calculate the position to center the label in the key
                font_scale = 1
                font = cv2.FONT_HERSHEY_SIMPLEX
                text_size = cv2.getTextSize(label, font, font_scale, 2)[0]
                text_x = x + (self.key_width - text_size[0]) // 2
                text_y = y + (self.key_height + text_size[1]) // 2

                # Draw the label on the key
                cv2.putText(self.keyboard_image, label, (text_x, text_y), font, font_scale, (255, 255, 255), 2)

from Assignment.HandTracking import HandTracking
from pynput.keyboard import Controller, Key
import numpy as np
import threading
import cv2


class OnScreenKeyboard:
    row_1 = [('Q', '1'), ('W', '2'), ('E', '3'), ('R', '4'), ('T', '5'),
             ('Z', '6'), ('U', '7'), ('I', '8'), ('O', '9'), ('P', '0')]
    row_2 = [('A', '@'), ('S', '#'), ('D', '$'), ('F', '_'), ('G', '&'), ('H', '-'), ('J', '+'), ('K', '('), ('L', ')')]
    row_3 = [('shift', '/'), ('Y', '*'), ('X', '"'), ('C', "'"), ('V', ':'),
             ('B', ';'), ('N', '!'), ('M', '?'), ('backspace', 'backspace')]
    row_4 = [('123', 'ABC'), ('space', 'space'), ('enter', 'enter')]

    def __init__(self) -> None:
        self.keys: list[list[(str, str)]] = [self.row_1, self.row_2, self.row_3, self.row_4]
        self.key_width, self.key_height = 100, 100
        self.start_x, self.start_y = 50, 50
        self.keyboard_image = np.zeros((600, 800, 3), dtype=np.uint8)
        self.is_numeric_mode = False  # Track if '123' is active

    def draw_keyboard(self, frame: np.ndarray) -> np.ndarray:
        self.keyboard_image = frame.copy()
        for i, row in enumerate(self.keys):
            for j, key in enumerate(row):
                x = self.start_x + j * self.key_width
                y = self.start_y + i * self.key_height

                # Draw a rectangle for the key
                cv2.rectangle(self.keyboard_image, (x, y), (x + self.key_width, y + self.key_height), (255, 255, 255),
                              2)

                # Determine the label for the key
                label = key[1] if self.is_numeric_mode else key[0]

                # Calculate the position to center the label in the key
                font_scale = 1
                font = cv2.FONT_HERSHEY_SIMPLEX
                text_size = cv2.getTextSize(str(label), font, font_scale, 2)[0]
                # Center the text of the keys
                text_x = x + (self.key_width - text_size[0]) // 2
                text_y = y + (self.key_height + text_size[1]) // 2

                # Draw the label on the key
                cv2.putText(self.keyboard_image, str(label), (text_x, text_y), font, font_scale, (255, 255, 255), 2)

        return self.keyboard_image

    def toggle_mode(self) -> None:
        """Toggle between alphanumeric and numeric/symbol mode"""
        self.is_numeric_mode = not self.is_numeric_mode

    def key_press(self, hands: list) -> None:
        pass


from concurrent.futures import ThreadPoolExecutor
from Assignment.HandTracking import HandTracking
from pynput.keyboard import Controller, Key
import numpy as np
import cv2


class OnScreenKeyboard:
    row_1 = [('q', 'Q', '1'), ('w', 'W', '2'), ('e', 'E', '3'), ('r', 'R', '4'), ('t', 'T', '5'),
             ('z', 'Z', '6'), ('u', 'U', '7'), ('i', 'I', '8'), ('o', 'O', '9'), ('p', 'P', '0')]
    row_2 = [('a', 'A', '@'), ('s', 'S', '#'), ('d', 'D', '$'), ('f', 'F', '_'), ('g', 'G', '&'),
             ('h', 'H', '-'), ('j', 'J', '+'), ('k', 'K', '('), ('l', 'L', ')')]
    row_3 = [('shift', 'shift', '/'), ('y', 'Y', '*'), ('x', 'X', '"'), ('c', 'C', "'"), ('v', 'V', ':'),
             ('b', 'B', ';'), ('n', 'N', '!'), ('m', 'M', '?'), ('backspace', 'backspace', 'backspace')]
    row_4 = [('123', '123', 'ABC'), ('space', 'space', 'space'), ('enter', 'enter', 'enter')]

    def __init__(self, detector: HandTracking().detector) -> None:
        self.keys: list[list[(str, str)]] = [self.row_1, self.row_2, self.row_3, self.row_4]
        self.key_width, self.key_height = 100, 100
        self.start_x, self.start_y = 50, 50
        self.keyboard_image = np.zeros((600, 800, 3), dtype=np.uint8)
        self.is_numeric_mode: bool = False  # Track if '123' is active
        self.is_shift_mode: bool = False  # Track if 'shift' is active
        self.hand_states: dict = {}
        self.controller = Controller()
        self.detector = detector
        self.executor = ThreadPoolExecutor(max_workers=4)

    def draw_keyboard(self, frame: np.ndarray) -> np.ndarray:
        self.keyboard_image: np.ndarray = frame.copy()

        def draw_row(row_data):
            i, row = row_data
            for j, key in enumerate(row):
                x: int = self.start_x + j * self.key_width
                y: int = self.start_y + i * self.key_height

                # Draw a rectangle for the key
                cv2.rectangle(self.keyboard_image, (x, y), (x + self.key_width, y + self.key_height),
                              (255, 255, 255), 2)

                label: str = key[2] if self.is_numeric_mode else (
                    key[1] if self.is_shift_mode and key[0] != 'shift' else key[0])

                # Calculate the position to center the label in the key
                font_scale: int = 1
                font: int = cv2.FONT_HERSHEY_SIMPLEX
                text_size = cv2.getTextSize(str(label), font, font_scale, 2)[0]
                # Center the text of the keys
                text_x: int = x + (self.key_width - text_size[0]) // 2
                text_y: int = y + (self.key_height + text_size[1]) // 2
                # Draw the label on the key
                cv2.putText(self.keyboard_image, str(label), (text_x, text_y), font, font_scale, (255, 255, 255), 2)
        # Parallelize the drawing of rows
        list(self.executor.map(draw_row, enumerate(self.keys)))

        return self.keyboard_image

    def toggle_numeric(self) -> None:
        """Toggle between alphanumeric and numeric/symbol mode"""
        self.is_numeric_mode: bool = not self.is_numeric_mode

    def toggle_shift(self) -> None:
        """Toggle between uppercase and lowercase characters"""
        self.is_shift_mode: bool = not self.is_shift_mode

    def key_press(self, hands: list) -> bool:
        if not hands:
            self.hand_states.clear()
            return False

        def process_hand(hand_data):
            hand_index, hand = hand_data
            landmark_list = hand["lmList"]
            x_index, y_index = landmark_list[8][:2]

            distance, _, _ = self.detector.findDistance(landmark_list[8][:2], landmark_list[4][:2], None)
            pressed_key = self.check_key_pressed(x_index, y_index)

            if hand_index not in self.hand_states:
                self.hand_states[hand_index] = False

            if distance < 30 and pressed_key and not self.hand_states[hand_index]:
                self.hand_states[hand_index] = True
                return self.handle_key_press(pressed_key)

            if distance >= 30:
                self.hand_states[hand_index] = False

            return False

        # Parallelize the drawing of processing hands
        indexed_hands = list(enumerate(hands))
        results = list(self.executor.map(process_hand, indexed_hands))
        return any(results)

    def handle_key_press(self, pressed_key: str) -> bool:
        if pressed_key in ('123', 'ABC'):
            self.toggle_numeric()
        elif pressed_key == 'shift':
            self.toggle_shift()
        elif pressed_key == 'space':
            self.controller.press(Key.space)
            self.controller.release(Key.space)
        elif pressed_key == 'enter':
            self.controller.press(Key.enter)
            self.controller.release(Key.enter)
        elif pressed_key == 'backspace':
            self.controller.press(Key.backspace)
            self.controller.release(Key.backspace)
        else:
            self.controller.press(pressed_key)
            self.controller.release(pressed_key)
        print(f"Pressed key: {pressed_key}")
        return True

    def check_key_pressed(self, x_finger, y_finger) -> str:
        for i, row in enumerate(self.keys):
            for j, key in enumerate(row):
                x = self.start_x + j * self.key_width
                y = self.start_y + i * self.key_height
                w, h = self.key_width, self.key_height

                # Check if the finger is within the key boundaries
                if (x <= x_finger <= x + w) and (y <= y_finger <= y + h):
                    if self.is_numeric_mode:
                        return key[2]  # Return numeric key
                    elif self.is_shift_mode and key[0] not in ('shift', 'space', 'backspace', 'enter'):
                        return key[1]  # Return uppercase key
                    else:
                        return key[0]  # Return lowercase key
        return ""

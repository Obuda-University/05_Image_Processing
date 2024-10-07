from pynput.keyboard import Controller, Key
from HandTracking import HandTracking
from Keyboard import KeyBoard
import numpy as np
import threading


class VirtualKeyboard:
    def __init__(self, layout: list[list[str]], hand_tracking: HandTracking) -> None:
        self.keyboard = KeyBoard(layout)
        self.keyboard_controller = Controller()
        self.hand_tracking = hand_tracking

    def process_input(self, hands: list) -> None:
        if hands:
            hand = hands[0]
            landmark_list = hand["lmList"]
            x_finger, y_finger = landmark_list[8][:2]  # Tip of right index finger
            pressed_key = self.keyboard.check_pressed_key(x_finger, y_finger)

            if pressed_key:
                self.handle_key_press(pressed_key, landmark_list)

    def handle_key_press(self, key, landmark_list: list) -> None:
        l, _, _ = self.hand_tracking.detector.findDistance(landmark_list[8][:2], landmark_list[4][:2], None)
        if l < 25:
            print(key)
            if key == 'space':
                self.keyboard_controller.press(Key.space)
            elif key == 'OK':
                self.keyboard_controller.press(Key.enter)
            else:
                self.keyboard_controller.press(key)
            # Use threading to release the key after a delay without blocking main execution
            threading.Thread(target=self.keyboard_controller.release, args=[key]).start()

    def draw(self, frame: np.ndarray) -> np.ndarray:
        return self.keyboard.draw_keyboard(frame)

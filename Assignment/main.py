from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller, Key
from Keyboard import KeyBoard
import concurrent.futures
import numpy as np
import threading
import cv2


class Camera:
    def __init__(self, width: int = 1280, height: int = 720, camera_id: int = 0) -> None:
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(3, width)
        self.cap.set(4, height)
        self.lock = threading.Lock()

    def read_frame(self) -> tuple[bool, [cv2.Mat, np.ndarray]]:
        with self.lock:
            success, frame = self.cap.read()
            return success, cv2.flip(frame, 1) if success else (False, None)

    def release(self) -> None:
        with self.lock:
            self.cap.release()
        cv2.destroyAllWindows()


class HandTracking:
    def __init__(self, max_hands: int = 4, detection_confidence: float = 0.8) -> None:
        self.detector = HandDetector(staticMode=False, maxHands=max_hands, detectionCon=detection_confidence)

    def detect_hands(self, frame: any) -> tuple[list, np.ndarray]:
        hands, frame = self.detector.findHands(frame, flipType=False)
        return hands, frame


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


class Application:
    def __init__(self) -> None:
        self.camera = Camera()
        self.hand_tracking = HandTracking()
        self.keyboard_layout: list[list[str]] = [['Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P',],
                                                 ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',],
                                                 ['Y', 'X', 'C', 'V', 'B', 'N', 'M',],
                                                 ['123', 'space', 'OK']]
        self.virtual_keyboard = VirtualKeyboard(self.keyboard_layout, self.hand_tracking)
        self.running: bool = True

    def run(self) -> None:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            while self.running:
                frame_future = executor.submit(self.camera.read_frame)
                success, frame = frame_future.result()
                if success:
                    hands_future = executor.submit(self.hand_tracking.detect_hands, frame)
                    hands, processed_frame = hands_future.result()

                    input_future = executor.submit(self.virtual_keyboard.process_input, hands)
                    input_future.result()

                    draw_future = executor.submit(self.virtual_keyboard.draw, processed_frame)
                    final_frame = draw_future.result()

                    cv2.imshow("Assignment", final_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.running = False
        self.stop()

    def stop(self) -> None:
        self.running = False
        self.camera.release()


if __name__ == "__main__":
    app = Application()
    app.run()

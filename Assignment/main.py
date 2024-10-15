from OnScreenKeyboard import OnScreenKeyboard
from HandTracking import HandTracking
from Camera import Camera
import concurrent.futures
import numpy as np
import time
import cv2


class Application:
    def __init__(self) -> None:
        self.camera = Camera()
        self.hand_tracking = HandTracking()
        self.onscreen_keyboard = OnScreenKeyboard(self.hand_tracking.detector)
        self.running: bool = True
        self._previous_time: int = 0

    def run(self) -> None:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            while self.running:
                frame_future = executor.submit(self.camera.read_frame)
                success, frame = frame_future.result()
                if success:
                    self.calc_frame_rate(frame)

                    hands_future = executor.submit(self.hand_tracking.detect_hands, frame)
                    hands, processed_frame = hands_future.result()

                    input_future = executor.submit(self.onscreen_keyboard.key_press, hands)
                    input_future.result()

                    draw_future = executor.submit(self.onscreen_keyboard.draw_keyboard, processed_frame)
                    final_frame = draw_future.result()

                    cv2.imshow("Assignment", final_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.running = False
        self.stop()

    def calc_frame_rate(self, img: np.ndarray) -> None:
        current_time: float = time.time()
        fps: float = 1 / (current_time - self._previous_time)
        self._previous_time = current_time
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

    def stop(self) -> None:
        self.running = False
        self.camera.release()


if __name__ == "__main__":
    app = Application()
    app.run()

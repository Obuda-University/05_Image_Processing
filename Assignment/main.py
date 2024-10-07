from VirtualKeyboard import VirtualKeyboard
from HandTracking import HandTracking
from Camera import Camera
import concurrent.futures
import cv2


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

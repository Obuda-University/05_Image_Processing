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

import numpy as np
import threading
import time
import cv2


class Camera:
    def __init__(self, width: int = 1280, height: int = 720, camera_id: int = 0, fps: int = 30) -> None:
        self.width: int = width
        self.height: int = height
        self.camera_id: int = camera_id
        self.fps: int = fps
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self._previous_time = time.time()
        self.lock = threading.Lock()

    def initialize(self) ->bool:
        """Initializes the camera, returns True if successful"""
        with self.lock:
            if not self.cap.isOpened():
                self.cap.open(self.camera_id)
            return self.cap.isOpened()

    def set_fps(self, fps: int) -> None:
        """Sets the camera's FPS"""
        with self.lock:
            self.fps = fps
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)

    def read_frame(self) -> tuple[bool, np.ndarray]:
        """Reads the frame from the camera"""
        with self.lock:
            success, frame = self.cap.read()
            if success:
                frame = cv2.flip(frame, 1)  # Flip horizontally
            return success, frame if success else (False, None)

    def release(self) -> None:
        """Releases camera resources"""
        with self.lock:
            if self.cap.isOpened():
                self.cap.release()
        cv2.destroyAllWindows()

    def set_resolution(self, width: int, height: int) -> None:
        """Sets the resolution of the camera"""
        with self.lock:
            self.width = width
            self.height = height
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    @staticmethod
    def process_frame(frame: np.ndarray) -> np.ndarray:
        """Optional frame processing, can be overridden or modified as needed"""
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def calc_frame_rate(self, frame: np.ndarray) -> None:
        """Calculates and displays the frame rate"""
        current_time = time.time()
        fps: float = 1 / (current_time - self._previous_time)
        self._previous_time = current_time
        cv2.putText(frame, f'FPS: {int(fps)}', (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)

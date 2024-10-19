import numpy as np
import threading
import cv2


class Camera:
    def __init__(self, width: int = 1280, height: int = 720, camera_id: int = 0) -> None:
        self.width: int = width
        self.height: int = height
        self.camera_id: int = camera_id
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.lock = threading.Lock()

    def initialize(self) ->bool:
        """Initializes the camera, returns True if successful"""
        with self.lock:
            if not self.cap.isOpened():
                self.cap.open(self.camera_id)
            return self.cap.isOpened()

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

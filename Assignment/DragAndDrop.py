from cvzone.HandTrackingModule import HandDetector
import numpy as np
import ctypes
import time
import cv2


# Constants
class Config:
    CAMERA_WIDTH, CAMERA_HEIGHT = 640, 480
    SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080


class DragAndDrop:
    def __init__(self) -> None:
        self.time_now = 0
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
        self.detector = HandDetector(staticMode=False, modelComplexity=0, maxHands=2, detectionCon=0.8, minTrackCon=0.5)

    def get_frame(self) -> [np.ndarray, None]:
        """Capture and flip the camera frame"""
        ret, frame = self.cap.read()
        return cv2.flip(frame, 1) if ret else None

    def get_frame_rate(self) -> int:
        """Calculate frame per second"""
        current_time = time.time()
        fps = int(1 / (current_time - self.time_now))
        self.time_now = current_time
        return fps

    def run(self) -> None:
        while True:
            frame = self.get_frame()
            if frame is None:
                break

            cv2.putText(frame, str(self.get_frame_rate()), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (128, 128, 128), 3)

            cv2.imshow('Frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':  # Entry point
    app = DragAndDrop()
    app.run()

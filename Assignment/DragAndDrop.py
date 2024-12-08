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
        self.cx, self.cy, self.w, self.h = 0, 0, 0, 0

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

    def detect_hand(self, img: np.ndarray) -> tuple[int, int, int]:
        """Detect hand(s) and control mouse based on gestures"""
        hands, _ = self.detector.findHands(img, flipType=False)
        color = (255, 0, 255)
        if hands:
            hand = hands[0]
            lm_list = hand["lmList"]

            index_finger_x, index_finger_y = lm_list[8][0], lm_list[8][1]
            if (100 < index_finger_x < 300) and (100 < index_finger_y < 300):
                color = (0, 255, 0)
        return color

    @staticmethod
    def draw_rectangle(frame: np.ndarray, color: tuple[int, int, int] = (255, 0, 255)) -> cv2.rectangle:
        return cv2.rectangle(frame, (100, 100), (300, 300), color, cv2.FILLED)

    def run(self) -> None:
        while True:
            frame = self.get_frame()
            if frame is None:
                break

            cv2.putText(frame, str(self.get_frame_rate()), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (128, 128, 128), 3)

            color = self.detect_hand(frame)
            self.draw_rectangle(frame, color)

            cv2.imshow('Frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':  # Entry point
    app = DragAndDrop()
    app.run()

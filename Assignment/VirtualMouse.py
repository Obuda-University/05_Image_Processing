from cvzone.HandTrackingModule import HandDetector
import HandTracking
import numpy as np
import ctypes
import time
import cv2


class VirtualMouse:
    def __init__(self) -> None:
        self.present_time = 0
        self.CAMERA_WIDTH = 640
        self.CAMERA_HEIGHT = 480
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.CAMERA_HEIGHT)
        self.detector = HandDetector(staticMode=False, modelComplexity=0, maxHands=2, detectionCon=0.8, minTrackCon=0.5)
        self.screen_width = 1920
        self.screen_height = 1080
        self.frame_reduction = 100

    def get_frame(self) -> np.ndarray:
        try:
            ret, frame = self.cap.read()
            frame = cv2.flip(frame, 1)
            return frame
        except Exception as e:
            print(e)

    def get_frame_rate(self) -> int:
        current_time = time.time()
        fps = int(1 / (current_time - self.present_time))
        self.present_time = current_time
        return fps

    def detect_hand(self, img: np.ndarray) -> None:
        hands, _ = self.detector.findHands(img, flipType=False)

        if hands:
            hand = hands[0]
            lm_list = hand["lmList"]

            x1, y1 = lm_list[8][:2]  # Index finger's x and y coordinates on camera frame

            x2, y2 = lm_list[4][:2]  # Thumb's x and y coordinates on camera frame

    def run(self) -> None:
        while True:
            frame = self.get_frame()
            cv2.putText(frame, str(self.get_frame_rate()), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (128, 128, 128), 3)
            self.detect_hand(frame)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # TODO: Check the gesture
    # TODO: Moving mode
    # TODO: Convert coordinates
    # TODO: Smoothen values
    # TODO: Move mouse
    # TODO: Clicking mode [predefined gesture]
    # TODO: Find distance [for gesture checking]
    # TODO: Click mouse

if __name__ == '__main__':
    app = VirtualMouse()
    app.run()

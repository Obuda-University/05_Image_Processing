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

    def move_mouse(self, index_finger) -> None:
        x_screen = int(np.interp(index_finger[0],
                                 (self.frame_reduction, self.CAMERA_WIDTH - self.frame_reduction),
                                 (0, self.screen_width)))
        y_screen = int(np.interp(index_finger[1],
                                 (self.frame_reduction, self.CAMERA_HEIGHT - self.frame_reduction),
                                 (0, self.screen_height)))
        ctypes.windll.user32.SetCursorPos(x_screen, y_screen)

    def detect_hand(self, img: np.ndarray) -> None:
        hands, _ = self.detector.findHands(img, flipType=False)

        if hands:
            hand = hands[0]
            lm_list = hand["lmList"]

            index: list[int, int] = lm_list[8][:2]  # Index finger's x and y coordinates on camera frame
            thumb: list[int, int] = lm_list[4][:2]  # Thumb's x and y coordinates on camera frame

            fingers = self.detector.fingersUp(hand)
            fingers[0] = 1 if fingers[0] == 0 else 0  # Fix thumb detection issue

            cv2.rectangle(img, (self.frame_reduction, self.frame_reduction),
                          (self.CAMERA_WIDTH - self.frame_reduction, self.CAMERA_HEIGHT - self.frame_reduction),
                          (255, 0, 255), 2)

            # if index is up and the rest is down, except the thumb [for click mode]
            move_mode: bool = fingers[1] == 1 and all(x == 0 for x in fingers[2:])
            if move_mode:  # Move mouse
                self.move_mouse(index)

            # if pointing with the middle finger and the others are closed
            click_mode: bool = fingers[0] == 0 and fingers[1] == 1 and all(x == 0 for x in fingers[2:])
            if click_mode:  # Click mouse
                length, frame, _ = self.detector.findDistance(index, thumb, img)
                #if length < 30:

    def run(self) -> None:
        while True:
            frame = self.get_frame()
            cv2.putText(frame, str(self.get_frame_rate()), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (128, 128, 128), 3)
            self.detect_hand(frame)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # TODO: Check the gesture
    # TODO: Smoothen values
    # TODO: Clicking mode [predefined gesture]
    # TODO: Find distance [for gesture checking]
    # TODO: Click mouse

if __name__ == '__main__':
    app = VirtualMouse()
    app.run()

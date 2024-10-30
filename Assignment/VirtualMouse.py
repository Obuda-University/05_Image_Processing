from cvzone.HandTrackingModule import HandDetector
import HandTracking
import numpy as np
import ctypes
import time
import cv2

# Constants
MOUSE_EVENT_LEFT_DOWN = 0x0002  # Left button down
MOUSE_EVENT_LEFT_UP = 0x0004    # Left button up

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
        self.smoothening_ratio = 6
        self.prev_location_x, self.prev_location_y = 0, 0
        self.curr_location_x, self.curr_location_y = 0, 0
        self.is_mouse_down = False
        self.last_click_time = 0
        self.click_cooldown = 0.3
        self.thumb_prev_state = None

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

    def move_mouse(self, index_finger: list[int, int]) -> None:
        x_screen = int(np.interp(index_finger[0],
                                 (self.frame_reduction, self.CAMERA_WIDTH - self.frame_reduction),
                                 (0, self.screen_width)))
        y_screen = int(np.interp(index_finger[1],
                                 (self.frame_reduction, self.CAMERA_HEIGHT - self.frame_reduction),
                                 (0, self.screen_height)))

        self.curr_location_x = int(self.prev_location_x + (x_screen - self.prev_location_x) / self.smoothening_ratio)
        self.curr_location_y = int(self.prev_location_y + (y_screen - self.prev_location_y) / self.smoothening_ratio)

        ctypes.windll.user32.SetCursorPos(self.curr_location_x, self.curr_location_y)
        self.prev_location_x, self.prev_location_y = self.curr_location_x, self.curr_location_y

    def click_double(self, index_finger_status: int, middle_finger_status: int) -> None:
        if index_finger_status == 1 and middle_finger_status == 1 and ((self.present_time - self.last_click_time) > self.click_cooldown):
            ctypes.windll.user32.mouse_event(MOUSE_EVENT_LEFT_DOWN, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(MOUSE_EVENT_LEFT_UP, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(MOUSE_EVENT_LEFT_DOWN, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(MOUSE_EVENT_LEFT_UP, 0, 0, 0, 0)
            self.last_click_time = self.present_time

    def click_hold(self, thumb_status: int) -> None:
        current_time = time.time()

        if self.thumb_prev_state is None:
            self.thumb_prev_state = thumb_status
            return

        if self.thumb_prev_state == 0 and thumb_status == 1:
            self.last_click_time = current_time
            self.is_mouse_down = False
        elif self.thumb_prev_state == 1 and thumb_status == 0:
            if (current_time - self.last_click_time) <= self.click_cooldown:
                ctypes.windll.user32.mouse_event(MOUSE_EVENT_LEFT_DOWN, 0, 0, 0, 0)
                ctypes.windll.user32.mouse_event(MOUSE_EVENT_LEFT_UP, 0, 0, 0, 0)
            else:
                ctypes.windll.user32.mouse_event(MOUSE_EVENT_LEFT_UP, 0, 0, 0, 0)
        elif thumb_status == 1 and not self.is_mouse_down:
            if (current_time - self.last_click_time) > self.click_cooldown:
                ctypes.windll.user32.mouse_event(MOUSE_EVENT_LEFT_DOWN, 0, 0, 0, 0)
                self.is_mouse_down = True
        self.thumb_prev_state = thumb_status

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
            # self.click_singe(fingers[0])
            self.click_double(fingers[1], fingers[2])
            self.click_hold(fingers[0])

    def run(self) -> None:
        while True:
            frame = self.get_frame()
            cv2.putText(frame, str(self.get_frame_rate()), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (128, 128, 128), 3)
            self.detect_hand(frame)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    app = VirtualMouse()
    app.run()

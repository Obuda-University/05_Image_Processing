from cvzone.HandTrackingModule import HandDetector
import numpy as np
import ctypes
import time
import cv2

# Constants
CAMERA_WIDTH, CAMERA_HEIGHT = 640, 480
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
FRAME_REDUCTION = 100
SMOOTHENING_RATIO = 6
CLICK_COOLDOWN = 0.3
MOUSE_EVENT_LEFT_DOWN = 0x0002  # Left button down
MOUSE_EVENT_LEFT_UP = 0x0004    # Left button up

# Utils
def _screen_coordinates(x, y, frame_reduction, cam_width, cam_height, screen_width, screen_height) -> [int, int]:
    """Interpolate (convert) camera coordinates to screen coordinates"""
    x_screen = int(np.interp(x, (frame_reduction, cam_width - frame_reduction), (0, screen_width)))
    y_screen = int(np.interp(y, (frame_reduction, cam_height - frame_reduction), (0, screen_height)))
    return x_screen, y_screen

def _is_cooldown_elapsed(last_action_time: float, cooldown: float) -> bool:
    """Checks if the predefined cooldown period has elapsed since the last action"""
    return (time.time() - last_action_time) > cooldown


class _Click:
    def __init__(self) -> None:
        self.thumb_prev_state = None
        self.last_click_time = 0
        self.present_time = 0
        self.is_mouse_down = False

    def double(self) -> None:
        ctypes.windll.user32.mouse_event(MOUSE_EVENT_LEFT_DOWN, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(MOUSE_EVENT_LEFT_UP, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(MOUSE_EVENT_LEFT_DOWN, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(MOUSE_EVENT_LEFT_UP, 0, 0, 0, 0)
        self.last_click_time = self.present_time

    def single_hold(self, thumb_status: int) -> None:
        current_time = time.time()

        if self.thumb_prev_state is None:
            self.thumb_prev_state = thumb_status
            return

        if self.thumb_prev_state == 0 and thumb_status == 1:
            self.last_click_time = current_time
            self.is_mouse_down = False
        elif self.thumb_prev_state == 1 and thumb_status == 0:
            if (current_time - self.last_click_time) <= CLICK_COOLDOWN:
                ctypes.windll.user32.mouse_event(MOUSE_EVENT_LEFT_DOWN, 0, 0, 0, 0)
                ctypes.windll.user32.mouse_event(MOUSE_EVENT_LEFT_UP, 0, 0, 0, 0)
            else:
                ctypes.windll.user32.mouse_event(MOUSE_EVENT_LEFT_UP, 0, 0, 0, 0)
        elif thumb_status == 1 and not self.is_mouse_down:
            if (current_time - self.last_click_time) > CLICK_COOLDOWN:
                ctypes.windll.user32.mouse_event(MOUSE_EVENT_LEFT_DOWN, 0, 0, 0, 0)
                self.is_mouse_down = True
        self.thumb_prev_state = thumb_status


class VirtualMouse:
    def __init__(self) -> None:
        self.time_now = 0
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        self.detector = HandDetector(staticMode=False, modelComplexity=0, maxHands=2, detectionCon=0.8, minTrackCon=0.5)
        self._prev_location_x, self._prev_location_y = 0, 0
        self._curr_location_x, self._curr_location_y = 0, 0
        self._last_click_time = 0
        self._click = _Click()

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

    def _move_mouse(self, index_finger: list[int, int]) -> None:
        """Move mouse cursor based on the index finger's position"""
        x_screen, y_screen = _screen_coordinates(index_finger[0], index_finger[1], FRAME_REDUCTION,
                                                 CAMERA_WIDTH, CAMERA_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)
        self._curr_location_x = int(self._prev_location_x + (x_screen - self._prev_location_x) / SMOOTHENING_RATIO)
        self._curr_location_y = int(self._prev_location_y + (y_screen - self._prev_location_y) / SMOOTHENING_RATIO)
        ctypes.windll.user32.SetCursorPos(self._curr_location_x, self._curr_location_y)
        self._prev_location_x, self._prev_location_y = self._curr_location_x, self._curr_location_y

    def _process_clicks(self, fingers: list[int]) -> None:
        """Process mouse clicks (single, double, hold) based on predefined gestures / states"""
        thumb_up, index_up, middle_up,  = fingers[0], fingers[1], fingers[2]
        current_time = time.time()
        if index_up and middle_up and _is_cooldown_elapsed(self._last_click_time, CLICK_COOLDOWN):
            self._click.double()
            self._last_click_time = current_time
        self._click.single_hold(thumb_up)

    def detect_hand(self, img: np.ndarray) -> None:
        """Detect hand(s) and control mouse based on gestures"""
        hands, _ = self.detector.findHands(img, flipType=False)
        if hands:
            hand = hands[0]
            lm_list = hand["lmList"]
            fingers: list[int] = self.detector.fingersUp(hand)
            fingers[0] = 1 if fingers[0] == 0 else 0  # Fix thumb detection issue
            index: list[int, int] = lm_list[8][:2]  # Index finger's x and y coordinates on camera frame
            # if index is up and the rest is down, except the thumb [for click mode]
            move_mode: bool = fingers[1] == 1 and all(x == 0 for x in fingers[2:])

            cv2.rectangle(img, (FRAME_REDUCTION, FRAME_REDUCTION),
                          (CAMERA_WIDTH - FRAME_REDUCTION, CAMERA_HEIGHT - FRAME_REDUCTION), (255, 0, 255), 2)

            if move_mode:
                self._move_mouse(index)
            self._process_clicks(fingers)

    def run(self) -> None:
        while True:
            frame = self.get_frame()
            if frame is None:
                break

            cv2.putText(frame, str(self.get_frame_rate()), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (128, 128, 128), 3)
            self.detect_hand(frame)
            cv2.imshow('Frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':  # Entry point
    app = VirtualMouse()
    app.run()

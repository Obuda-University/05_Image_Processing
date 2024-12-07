from cvzone.HandTrackingModule import HandDetector
import numpy as np
import ctypes
import time
import cv2


class Config:
    SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
    SMOOTHENING_RATIO = 6
    CLICK_COOLDOWN = 0.3
    MOUSE_EVENT_LEFT_DOWN = 0x0002  # Left button down
    MOUSE_EVENT_LEFT_UP = 0x0004    # Left button up


# Utils
def _screen_coordinates(x, y, rect_x1, rect_x2, rect_y1, rect_y2) -> [int, int]:
    """Map camera coordinates to screen coordinates with frame reduction applied"""
    x_screen = int(np.interp(x, (rect_x1, rect_x2), (0, Config.SCREEN_WIDTH)))
    y_screen = int(np.interp(y, (rect_y1, rect_y2), (0, Config.SCREEN_HEIGHT)))
    return x_screen, y_screen


def _is_cooldown_elapsed(last_action_time: float, cooldown: float = Config.CLICK_COOLDOWN) -> bool:
    """Checks if the predefined cooldown period has elapsed since the last action"""
    return (time.time() - last_action_time) > cooldown


def _click_event(down: bool = True) -> None:
    """Perform mouse pressing action"""
    event = Config.MOUSE_EVENT_LEFT_DOWN if down else Config.MOUSE_EVENT_LEFT_UP
    try:
        ctypes.windll.user32.mouse_event(event, 0, 0, 0, 0)
    except Exception as e:
        print(e)


class _ClickHandler:
    def __init__(self) -> None:
        self.thumb_prev_state = None
        self.last_click_time = 0
        self.is_mouse_down = False

    def double(self) -> None:
        """Simulate double click"""
        _click_event(True)
        _click_event(False)
        _click_event(True)
        _click_event(False)
        self.last_click_time = time.time()

    def single(self) -> None:
        """Simulate single click"""
        _click_event(True)
        _click_event(False)
        self.last_click_time = time.time()

    def hold(self) -> None:
        """Simulate holding the left mouse button"""
        if not self.is_mouse_down:
            _click_event(True)
            self.is_mouse_down = True

    def release_hold(self) -> None:
        """Release holding the left mouse button"""
        if self.is_mouse_down:
            _click_event(False)
            self.is_mouse_down = False

    def process_thumb_gesture(self, thumb_status: int) -> None:
        """Decide single-click or hold based on the thumb status"""
        current_time = time.time()

        if self.thumb_prev_state is None:
            self.thumb_prev_state = thumb_status
            return

        if self.thumb_prev_state == 0 and thumb_status == 1:
            self.last_click_time = current_time
            self.is_mouse_down = False
        elif self.thumb_prev_state == 1 and thumb_status == 0:
            if (current_time - self.last_click_time) <= Config.CLICK_COOLDOWN:
                self.single()
            else:
                self.release_hold()
        elif thumb_status == 1:
            if _is_cooldown_elapsed(self.last_click_time):
                self.hold()
        self.thumb_prev_state = thumb_status


class VirtualMouse:
    def __init__(self) -> None:
        self.detector = HandDetector(staticMode=False, modelComplexity=0, maxHands=2, detectionCon=0.8, minTrackCon=0.5)
        self._prev_location_x, self._prev_location_y = 0, 0
        self._curr_location_x, self._curr_location_y = 0, 0
        self._last_click_time = 0
        self._click = _ClickHandler()
        self.rect_coords = None

    def _move_mouse(self, index_finger: list[int, int]) -> None:
        """Move mouse cursor based on the index finger's position"""
        if self.rect_coords is None:
            return

        x1, x2, y1, y2 = self.rect_coords
        x, y = index_finger

        # Check if index finger is within the rectangle
        if x1 <= x <= x2 and y1 <= y <= y2:
            x_screen, y_screen = _screen_coordinates(x, y, x1, x2, y1, y2)

            # Smoothen mouse movement
            self._curr_location_x = int(
                self._prev_location_x + (x_screen - self._prev_location_x) / Config.SMOOTHENING_RATIO)
            self._curr_location_y = int(
                self._prev_location_y + (y_screen - self._prev_location_y) / Config.SMOOTHENING_RATIO)

            ctypes.windll.user32.SetCursorPos(self._curr_location_x, self._curr_location_y)
            self._prev_location_x, self._prev_location_y = self._curr_location_x, self._curr_location_y

    def _process_clicks(self, fingers: list[int]) -> bool:
        """Process mouse clicks (single, double, hold) based on predefined gestures / states"""
        thumb_up, index_up, middle_up = fingers[0], fingers[1], fingers[2]
        current_time = time.time()
        if index_up and middle_up and _is_cooldown_elapsed(self._last_click_time, Config.CLICK_COOLDOWN):
            self._click.double()
            self._last_click_time = current_time
            return True
        self._click.process_thumb_gesture(thumb_up)
        return False

    def draw_rectangle(self, img: np.ndarray, cam_width: int, cam_height: int) -> tuple:
        """Draw a smaller rectangle in the middle of the frame."""
        rect_width, rect_height = 240, 135
        x1 = (cam_width // 2) - (rect_width // 2)
        y1 = (cam_height // 2) - (rect_height // 2)
        x2 = x1 + rect_width
        y2 = y1 + rect_height
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
        self.rect_coords = (x1, x2, y1, y2)
        return self.rect_coords

    def detect_hand(self, img: np.ndarray) -> [bool, float, float]:
        """Detect hand(s) and control mouse based on gestures"""
        hands, _ = self.detector.findHands(img, flipType=False)
        if hands:
            hand = hands[0]
            lm_list = hand["lmList"]
            fingers: list[int] = self.detector.fingersUp(hand)
            fingers[0] = 1 if fingers[0] == 0 else 0  # Fix thumb detection

            index: list[int, int] = lm_list[8][:2]  # Index finger's x and y coordinates on camera frame
            # if index is up and the rest is down, except the thumb [for click mode]
            move_mode: bool = fingers[1] == 1 and all(x == 0 for x in fingers[2:])

            self.draw_rectangle(img, img.shape[1], img.shape[0])

            if move_mode:
                self._move_mouse(index)
            clicked = self._process_clicks(fingers)

            return clicked, fingers[0], fingers[1]
        return False, 0.0, 0.0

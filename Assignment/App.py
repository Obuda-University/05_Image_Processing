from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller
import numpy as np
import cv2 as cv
import win32gui
import win32con
import win32api
import ctypes
import time


# region Utils
cap = cv.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)
detector = HandDetector(detectionCon=0.7)
controller = Controller()
current_x, current_y = 0, 0
prev_x, prev_y = 0, 0
smooth_ratio = 6
cooldown = 0.5
# endregion


# region Camera
def get_camera() -> np.ndarray:
    success, frame = cap.read()
    if success:
        frame = cv.flip(frame, 1)
        return frame
    return np.zeros((240, 320, 3), dtype=np.uint8)


def draw_helper_rectangle(camera_frame) -> tuple:
    rect_width, rect_height = 240, 135
    x1 = (320 // 2) - (rect_width // 2)
    y1 = (240 // 2) - (rect_height // 2)
    x2 = x1 + rect_width
    y2 = y1 + rect_height
    cv.rectangle(camera_frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
    return x1, x2, y1, y2
# endregion


# region Keyboard
def get_kbd() -> np.ndarray:
    return np.ones((400, 800, 3), dtype=np.uint8)


def is_within_keyboard(mouse_x, mouse_y, kbd_pos, kbd_size) -> bool:
    kbd_x, kbd_y = kbd_pos
    kbd_width, kbd_height = kbd_size
    return (kbd_x <= mouse_x <= kbd_x + kbd_width) and (kbd_y <= mouse_y <= kbd_y + kbd_height)


def is_key_press(fingers: list[int]) -> bool:
    """Checks if index finger and pinky is up -> pressing a key"""
    fingers[0] = 1 if fingers[0] == 0 else 0  # Fix thumb detection
    return True if (fingers[1] == 1 and fingers[4] == 1) else False
# endregion


# region Mouse
def get_screen_coordinates(x, y, rect_x1, rect_x2, rect_y1, rect_y2) -> [int, int]:
    """Map camera coordinates to screen coordinates with frame reduction applied"""
    x_screen = int(np.interp(x, (rect_x1, rect_x2), (0, 1920)))
    y_screen = int(np.interp(y, (rect_y1, rect_y2), (0, 1080)))
    return x_screen, y_screen


def is_moving_mouse(fingers: list[int]) -> bool:
    """Checks if only index finger is up -> Moving the mouse"""
    fingers[0] = 1 if fingers[0] == 0 else 0  # Fix thumb detection
    return True if fingers[1] == 1 and all(x == 0 for i, x in enumerate(fingers) if i != 1) else False


def move_mouse(rectangle_coords: tuple, index_pos: tuple) -> None:
    global current_x, current_y, prev_x, prev_y
    x1, x2, y1, y2 = rectangle_coords
    x, y = index_pos

    if x1 <= x <= x2 and y1 <= y <= y2:  # Check if index finger is within the rectangle
        x_screen, y_screen = get_screen_coordinates(x, y, x1, x2, y1, y2)

        current_x = int(prev_x + (x_screen - prev_x) / smooth_ratio)
        current_y = int(prev_y + (y_screen - prev_y) / smooth_ratio)

        ctypes.windll.user32.SetCursorPos(current_x, current_y)
        prev_x, prev_y = current_x, current_y
# endregion


# region Window
def get_hands(frame: np.ndarray) -> list:
    hands, _ = detector.findHands(frame, flipType=False)
    return hands


def create_window(camera_frame: np.ndarray, cam_pos: tuple, kbd_frame: np.ndarray, kbd_pos: tuple) -> np.ndarray:
    frame: np.ndarray = np.zeros((1080, 1920, 3), dtype=np.uint8)  # Main Canvas
    cv.rectangle(frame, (0, 0), (1920 - 1, 1080 - 1), (0, 0, 255), 2)  # Border Lines

    # Handle Keyboard Frame
    width, height = 800, 400
    kbd_x_offset, kbd_y_offset = kbd_pos
    if (0 <= kbd_x_offset <= 1920 - width) and (0 <= kbd_y_offset <= 1080 - height):  # Ensure keyboard frame fitting
        frame[kbd_y_offset:kbd_y_offset + height, kbd_x_offset:kbd_x_offset + width] = kbd_frame

    # Handle Camera Frame
    cam_x_offset, cam_y_offset = cam_pos
    if (0 <= cam_x_offset <= 1920 - 320) and (0 <= cam_y_offset <= 1080 - 240):  # Ensure camera frame fitting
        frame[cam_y_offset:cam_y_offset + 240, cam_x_offset:cam_x_offset + 320] = camera_frame

    return frame


def set_window_properties(window_name: str) -> None:
    cv.namedWindow(window_name, cv.WINDOW_NORMAL)
    cv.setWindowProperty(window_name, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    user32 = ctypes.windll.user32
    hwnd = win32gui.FindWindow(None, window_name)

    # Always on top
    win32gui.SetWindowPos(
        hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
    )

    # Transparent window
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)
# endregion


def terminate_application():
    cap.release()
    cv.destroyAllWindows()


def main_loop() -> None:
    camera_x, camera_y = 1598, 790
    kbd_x, kbd_y = 700, 630
    kbd_width, kbd_height = 800, 400
    last_press_time = 0.0
    window_name = "Camera Frame"
    set_window_properties(window_name)

    while True:
        camera_frame = get_camera()
        kbd_frame = get_kbd()
        hands = get_hands(camera_frame)
        mouse_x, mouse_y = win32api.GetCursorPos()

        if hands:  # Hands are detected
            rectangle_coords = draw_helper_rectangle(camera_frame)
            hand = hands[0]
            lm_list = hand["lmList"]
            fingers_up = detector.fingersUp(hand)

            # Move mouse if the index finger is pointing
            if is_moving_mouse(fingers_up):
                move_mouse(rectangle_coords, lm_list[8][:2])
            # Press key if within the keyboard
            current_time = time.time()
            if is_key_press(fingers_up):
                if is_within_keyboard(mouse_x, mouse_y, (kbd_x, kbd_y), (kbd_width, kbd_height)):
                    if current_time - last_press_time > cooldown:
                        controller.press('a')
                        controller.release('a')
                        last_press_time = current_time

        window_frame = create_window(camera_frame, (camera_x, camera_y), kbd_frame, (kbd_x, kbd_y))
        cv.imshow("Camera Frame", window_frame)

        key = cv.waitKey(1)
        if key & 0xFF == ord('q'):
            break
    terminate_application()


main_loop()

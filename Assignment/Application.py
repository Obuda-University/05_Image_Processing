from cvzone.HandTrackingModule import HandDetector
from OnScreenKeyboard import OnScreenKeyboard
from VirtualMouse import VirtualMouse
from Camera import Camera
import concurrent.futures
import numpy as np
import win32gui
import win32con
import win32api
import ctypes
import cv2

# Define Windows API Constants
WS_EX_TRANSPARENT: hex = 0x00000020  # Create a transparent window and mouse events are passed through
WS_EX_LAYERED: hex = 0x00080000  # Allows transparency and alpha blending
WS_EX_TOPMOST: hex = 0x00000008  # The window wil be always on the top no matter what
GWL_EX_STYLE: int = -20  # To read or modify the window styles

user32 = ctypes.windll.user32  # Load the user32.dll
user32.SetWindowLongPtrW.restype = ctypes.c_long
user32.SetWindowLongPtrW.argtype = [ctypes.c_void_p, ctypes.c_int, ctypes.c_long]

CAMERA_WIDTH, CAMERA_HEIGHT = 320, 240


class Application:
    def __init__(self) -> None:
        self.window_name: str = "Computer Vision Assignment"
        self.is_running: bool = True
        self.hwnd: any = None
        self.screen_width: int = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.screen_height: int = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        self.camera = Camera(CAMERA_WIDTH, CAMERA_HEIGHT, 0, 60)
        self.camera.set_fps(60)
        self.detector = HandDetector(staticMode=False, modelComplexity=1, maxHands=2, detectionCon=0.8, minTrackCon=0.5)
        self.mouse = VirtualMouse()
        self.kbd = OnScreenKeyboard()

    def _make_click_through(self, enable: bool) -> None:
        """Make the window click-through by modifying its style"""
        if self.hwnd is None:
            self.hwnd = win32gui.FindWindow(None, self.window_name)  # Get the window handle

        if self.hwnd:
            # Set the window style to layered, transparent, and topmost
            styles = win32gui.GetWindowLong(self.hwnd, GWL_EX_STYLE)
            if enable:
                styles = styles | WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOPMOST
            else:
                styles = styles & ~WS_EX_TRANSPARENT

            user32.SetWindowLongPtrW(self.hwnd, GWL_EX_STYLE, styles)
            # Set transparent color key
            win32gui.SetLayeredWindowAttributes(self.hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)

    def _draw_buttons(self, frame: np.ndarray) -> dict:
        """Draw buttons on the frame"""
        radius: int = 20
        fill = cv2.FILLED
        x_pos: int = int(self.screen_width * 0.98)
        button_positions: dict = {
            'Exit': (x_pos, int(self.screen_height * 0.45), (0, 0, 255), 'X'),
            'Keyboard': (x_pos, int(self.screen_height * 0.5), (255, 0, 0), 'K'),
            'Options': (x_pos, int(self.screen_height * 0.55), (0, 255, 0), 'O')  # might delete later
        }

        button_rects: dict = {}  # Store button rectangles for click detection

        for i, (x, y, color, text) in button_positions.items():
            cv2.circle(frame, (x, y), radius, color, fill)
            cv2.putText(frame, text, (x - 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),
                        2, cv2.LINE_AA)
            button_rects[i] = (x, y, radius)

        return button_rects

    def _draw_camera_frame(self, frame: np.ndarray, camera_frame: np.ndarray) -> None:
        if camera_frame is not None:
            camera_height, camera_width, _ = camera_frame.shape
            top_left = (self.screen_width - camera_width, self.screen_height - camera_height - 50)
            bottom_right = (self.screen_width, self.screen_height - 50)
            frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = camera_frame

    def _camera(self) -> tuple[bool, np.ndarray]:
        """Fetch the camera frame."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            frame_future = executor.submit(self.camera.read_frame)
            return frame_future.result()

    @staticmethod
    def _is_inside_button(mouse_pos: tuple[int, int], button_pos: tuple[int, int], radius: int) -> bool:
        """Check if mouse position is inside the button"""
        return (mouse_pos[0] - button_pos[0]) ** 2 + (mouse_pos[1] - button_pos[1]) ** 2 <= radius ** 2

    def _handle_click(self, mouse_x: int, mouse_y: int, buttons: dict) -> None:
        """Handle mouse click events"""
        for button_id, (x, y, radius) in buttons.items():
            if self._is_inside_button((mouse_x, mouse_y), (x, y), radius):
                if button_id == 'Exit':
                    self.stop()
                elif button_id == 'Keyboard':
                    self.kbd.is_visible = not self.kbd.is_visible
                elif button_id == 'Options':
                    print("MENU")
                    # Show Menu

    def _create_window(self) -> None:
        """Create and configure the application window"""
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.resizeWindow(self.window_name, self.screen_width, self.screen_height)

        self.hwnd = win32gui.FindWindow(None, self.window_name)

        if self.hwnd:
            self._make_click_through(True)
        else:
            print("[ERROR]: Failed to retrieve window handle.")

    def stop(self) -> None:
        self.camera.release()
        self.is_running = False
        self.hwnd = None

    def run(self) -> None:
        """Run the main application loop"""
        self._create_window()

        while self.is_running:
            # Create a transparent image
            frame: np.ndarray = np.zeros((self.screen_height, self.screen_width, 3), dtype=np.uint8)
            cv2.rectangle(frame, (0, 0), (self.screen_width - 1, self.screen_height - 1), (0, 0, 255), 2)
            buttons: dict = self._draw_buttons(frame)

            success, camera_frame = self._camera()
            if success and camera_frame is not None:
                self.camera.calc_frame_rate(camera_frame)

                clicked = self.mouse.detect_hand(camera_frame)
                self._draw_camera_frame(frame, camera_frame)

                mouse_x, mouse_y = win32api.GetCursorPos()
                if clicked[0] is True:
                    self._handle_click(mouse_x, mouse_y, buttons)

                    if self.kbd.is_visible:
                        self.kbd.key_press(mouse_x, mouse_y)

                if self.kbd.is_visible:
                    kbd_frame = self.kbd.draw_keyboard(frame)
                    mask = (kbd_frame > 0).any(axis=2)
                    frame[mask] = kbd_frame[mask]
                    # self._make_click_through(False)
                # else:
                    # self._make_click_through(True)
            else:
                print("[ERROR]: Failed to read camera frame")

            cv2.imshow(self.window_name, frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                self.stop()

            # Ensure the window stays on top
            if self.hwnd is not None and win32gui.IsWindow(self.hwnd):
                win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        cv2.destroyAllWindows()


if __name__ == '__main__':
    app = Application()
    app.run()

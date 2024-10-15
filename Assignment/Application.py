import numpy as np
import cv2
import win32gui
import win32con
import win32api
import ctypes

# Define Windows API Constants
WS_EX_TRANSPARENT: hex = 0x00000020  # Create a transparent window and mouse events are passed through
WS_EX_LAYERED: hex = 0x00080000  # Allows transparency and alpha blending
WS_EX_TOPMOST: hex = 0x00000008  # The window wil be always on the top no matter what
GWL_EX_STYLE: int = -20  # To read or modify the window styles

user32 = ctypes.windll.user32  # Load the user32.dll
user32.SetWindowLongPtrW.restype = ctypes.c_long
user32.SetWindowLongPtrW.argtype = [ctypes.c_void_p, ctypes.c_int, ctypes.c_long]


class Application:
    def __init__(self):
        self.window_name = "Computer Vision Assignment"
        self.is_running = True
        self.hwnd = None

    def _make_click_through(self):
        self.hwnd = win32gui.FindWindow(None, self.window_name)  # Get the window handle

        # Set the window style to layered, transparent, and topmost
        styles = win32gui.GetWindowLong(self.hwnd, GWL_EX_STYLE)
        styles = styles | WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOPMOST
        user32.SetWindowLongPtrW(self.hwnd, GWL_EX_STYLE, styles)

        win32gui.SetLayeredWindowAttributes(self.hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)

    def _create_window(self) -> None:
        self.screen_width: int = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.screen_height: int = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.resizeWindow(self.window_name, self.screen_width, self.screen_height)

        self._make_click_through()

    def run(self) -> None:
        self._create_window()

        while self.is_running:
            # Create a transparent image
            frame = np.zeros((self.screen_height, self.screen_width, 3), dtype=np.uint8)
            cv2.rectangle(frame, (0, 0), (self.screen_width - 1, self.screen_height - 1), (0, 0, 255), 2)

            cv2.rectangle(frame, (self.screen_width - 100, 0), (self.screen_width, 50), (0, 0, 255), -1)
            cv2.putText(frame, "Exit", (self.screen_width - 80, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow(self.window_name, frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                self.is_running = False

            cursor_pos = win32gui.GetCursorPos()
            if self.screen_width - 100 <= cursor_pos[0] <= self.screen_width and 0 <= cursor_pos[1] <= 50:
                if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) & 0x8000:
                    self.is_running = False

            # Ensure the window stays on top
            win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        cv2.destroyAllWindows()


if __name__ == '__main__':
    app = Application()
    app.run()
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
    def __init__(self) -> None:
        self.window_name: str = "Computer Vision Assignment"
        self.is_running: bool = True
        self.hwnd: any = None
        self.screen_width: int = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.screen_height: int = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    def _make_click_through(self) -> None:
        """Make the window click-through by modifying its style"""
        self.hwnd = win32gui.FindWindow(None, self.window_name)  # Get the window handle

        # Set the window style to layered, transparent, and topmost
        styles = win32gui.GetWindowLong(self.hwnd, GWL_EX_STYLE)
        styles = styles | WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOPMOST
        user32.SetWindowLongPtrW(self.hwnd, GWL_EX_STYLE, styles)

        # Set transparent color key
        win32gui.SetLayeredWindowAttributes(self.hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)

    def _draw_buttons(self, frame: np.ndarray) -> None:
        """Draw buttons on the frame"""
        radius: int = 20
        fill = cv2.FILLED
        x_pos: int = int(self.screen_width * 0.98)
        button_positions: dict = {
            'Exit': (x_pos, int(self.screen_height * 0.45), (0, 0, 255), 'X'),
            'Keyboard': (x_pos, int(self.screen_height * 0.5), (255, 0, 0), 'K'),
            'Options': (x_pos, int(self.screen_height * 0.55), (0, 255, 0), 'O')  # might delete later
        }

        for i, (x, y, color, text) in button_positions.items():
            cv2.circle(frame, (x, y), radius, color, fill)
            cv2.putText(frame, text, (x - 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),
                        2, cv2.LINE_AA)

    def _create_window(self) -> None:
        """Create and configure the application window"""
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.resizeWindow(self.window_name, self.screen_width, self.screen_height)

        self._make_click_through()

    def run(self) -> None:
        """Run the main application loop"""
        self._create_window()

        while self.is_running:
            # Create a transparent image
            frame: np.ndarray = np.zeros((self.screen_height, self.screen_width, 3), dtype=np.uint8)
            cv2.rectangle(frame, (0, 0), (self.screen_width - 1, self.screen_height - 1), (0, 0, 255), 2)

            self._draw_buttons(frame)

            cv2.imshow(self.window_name, frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                self.is_running = False

            # Ensure the window stays on top
            win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        cv2.destroyAllWindows()


if __name__ == '__main__':
    app = Application()
    app.run()
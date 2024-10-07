import cv2


class Key_OLD:
    def __init__(self, pos: tuple[int, int], text: str, size: list[int] = None):
        self.size = size if size else [100, 100]
        self.pos = pos
        self.text = text
        self.hovered = False

    def draw_key(self, img) -> any:
        x, y = self.pos
        w, h = self.size

        if self.hovered:
            w += 15
            h += 15
            alpha: float = 0
        else:
            alpha: float = 0.5

        overlay = img.copy()  # For opacity control
        cv2.rectangle(img, self.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
        # Apply transparency
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
        # Center text inside the button
        font_scale: int = 4
        thickness: int = 4
        text_size = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_PLAIN, font_scale, thickness)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2

        cv2.putText(img, self.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, font_scale, (255, 255, 255), thickness)

        return img

    def is_pressed(self, x_finger, y_finger) -> bool:
        x, y = self.pos
        w, h = self.size
        if (x < x_finger < x + w) and (y < y_finger < y + h):
            self.hovered = True
            return True
        else:
            self.hovered = False
        return False

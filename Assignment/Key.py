import cv2


class Key:
    def __init__(self, pos: (int, int), text: str, size: [list[int, int], None]):
        if size is None:
            self.size = [100, 100]
        else:
            self.size = size
        self.pos = pos
        self.text = text

    def draw_key(self, img) -> any:
        x, y = self.pos
        w, h = self.size
        cv2.rectangle(img, self.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, self.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

        return img

    def is_pressed(self, x_finger, y_finger) -> bool:
        x, y = self.pos
        w, h = self.size
        if (x < x_finger < x + w) and (y < y_finger < y + h):
            return True
        return False

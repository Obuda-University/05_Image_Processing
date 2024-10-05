from Key import Key


class KeyBoard:
    def __init__(self, list_of_keys: list[list[str]]) -> None:
        self.keys: list = []
        self.create_keyboard(list_of_keys)

    def create_keyboard(self, list_of_keys: list[list[str]]) -> None:
        key_x_start, key_y_start = 100, 100
        key_width, key_height = 85, 85
        spacing: int = 10

        for row_idx, row in enumerate(list_of_keys):
            for col_idx, key_text in enumerate(row):
                x = key_x_start + col_idx * (key_width + spacing)
                y = key_y_start + row_idx * (key_height + spacing)
                self.keys.append(Key((x, y), key_text, [key_width, key_height]))

    def draw_keyboard(self, img: any) -> any:
        for key in self.keys:
            img = key.draw_key(img)
        return img

    def check_pressed_key(self, x_finger, y_finger) -> [str, None]:
        for key in self.keys:
            if key.is_pressed(x_finger, y_finger):
                return key.text
        return None

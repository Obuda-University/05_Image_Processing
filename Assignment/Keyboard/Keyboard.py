from Key import Key


class KeyBoard:
    def __init__(self, list_of_keys: list[list[str]]) -> None:
        self.keys: list[Key] = []
        self.create_keyboard(list_of_keys)

    def create_keyboard(self, list_of_keys: list[list[str]]) -> None:
        key_width, key_height = 86, 86
        spacing: int = 20
        screen_width: int = 1280
        screen_height: int = 720

        # Calculate the indentation of rows (As on mobile phone)
        row_starts: list[int] = [
            (screen_width - len(list_of_keys[0]) * (key_width + spacing)) // 2,
            (screen_width - len(list_of_keys[1]) * (key_width + spacing)) // 2,
            (screen_width - len(list_of_keys[2]) * (key_width + spacing)) // 2,
            (screen_width - len(list_of_keys[3]) * (key_width + spacing)) // 2,
        ]
        # Bottom with padding
        key_y_start: int = screen_height - 4 * (key_height + spacing) - 100

        # Precalculate x positions
        q_key_x: int = row_starts[0]
        c_key_x: int = row_starts[2] + 2 * (key_width + spacing)
        o_key_x: int = row_starts[0] + 8 * (key_width + spacing) + 43

        for row_idx, row in enumerate(list_of_keys):
            if row_idx < 3:
                key_x_start: int = row_starts[row_idx]
            else:  # Centered for special row
                key_x_start: int = (screen_width - len(row) * (key_width + spacing)) // 2

            for col_idx, key_text in enumerate(row):
                x: int = key_x_start + col_idx * (key_width + spacing)
                y: int = key_y_start + row_idx * (key_height + spacing)

                # Handle special keys
                if key_text == 'space':
                    x = c_key_x
                    space_width = 4 * (key_width + spacing) - spacing
                    self.keys.append(Key((x, y), key_text, [space_width, key_height]))
                elif key_text == '123':
                    x = q_key_x
                    self.keys.append(Key((x, y), key_text, [key_width * 2 - spacing, key_height]))
                elif key_text == 'OK':
                    x = o_key_x
                    self.keys.append(Key((x, y), key_text, [key_width * 2 - spacing, key_height]))
                else:
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

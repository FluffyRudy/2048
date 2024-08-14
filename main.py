import readchar


class Manager2048:
    def __init__(self):
        self.grid = [[0, 0, 2, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.max_rows, self.max_cols = len(self.grid), len(self.grid[0])
        self.shift_x = 0
        self.shift_y = 0
        self.isover = False
        self.key_map_vertl = {
            readchar.key.UP: -1,
            readchar.key.DOWN: +1,
        }
        self.key_map_hrztl = {
            readchar.key.LEFT: -1,
            readchar.key.RIGHT: 1,
        }

    def display_table(self):
        for row in self.grid:
            line_length = len(row) * 3 + 2
            print("_" * line_length)
            print("|" + " | ".join(map(str, row)) + "|")
        print("‾" * line_length)

    def reset_shift(self):
        self.shift_x = 0
        self.shift_y = 0

    def is_valid_position(self, row: int, col: int):
        return (
            (0 <= row < self.max_rows)
            and (0 <= col < self.max_cols)
            and self.grid[row][col] == 0
        )

    def shift_blocks(self, shift_x: int, shift_y: int):
        pass

    def handle_input(self):
        key = readchar.readkey()
        self.listen_for_exit(key)

        if not self.isover:
            self.shift_x = self.key_map_hrztl.get(key, 0)
            self.shift_y = self.key_map_vertl.get(key, 0)

            if self.shift_x or self.shift_y:
                self.display_table()
                self.reset_shift()

    def listen_for_exit(self, key: bytes):
        is_quitting = key == "q"
        if is_quitting:
            self.isover = True
        return self.isover

    def run(self):
        while not self.isover:
            self.handle_input()

    def get_board(self) -> list[list[int]]:
        return self.grid

    def set_board(self, board: list[list[int]]):
        self.grid = board

    def get_dimension(self) -> tuple[int, int]:
        return self.max_rows, self.max_cols


def main():
    game_2048 = Manager2048()
    game_2048.run()


if __name__ == "__main__":
    main()

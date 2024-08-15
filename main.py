import readchar
from enum import Enum, auto
from os import system


class MovementType(Enum):
    NULL_SHIFT = auto()
    SHIFT_DONE = auto()
    NO_SLOT = auto()


class Manager2048:
    def __init__(self):
        self.grid = [[0, 0, 2, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2]]
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
        self.clear_window()
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

    def get_block_at(self, row: int, col: int):
        return self.grid[row][col]

    def get_farthest_row(self, shift_y: int, row: int, col: int) -> int:
        new_row = row + shift_y

        if new_row >= self.max_rows or new_row < 0:
            return row
        if self.grid[new_row][col] != 0:
            return row
        return self.get_farthest_row(shift_y, new_row, col)

    def shift_blocks(self, shift_x: int, shift_y: int) -> MovementType:
        if shift_x == 0 and shift_y == 0:
            return MovementType.NULL_SHIFT

        blocks_moved = False
        for rowidx, blockrow in enumerate(self.grid):
            for colidx, block in enumerate(blockrow):
                if block == 0:
                    continue
                new_row = self.get_farthest_row(shift_y, rowidx, colidx)
                new_col = colidx + shift_x
                if self.is_valid_position(new_row, new_col):
                    self.grid[new_row][new_col] = block
                    self.grid[rowidx][colidx] = 0
                    blocks_moved = True

        return MovementType.SHIFT_DONE if blocks_moved else MovementType.NO_SLOT

    def handle_input(self):
        key = readchar.readkey()
        self.listen_for_exit(key)

        if not self.isover:
            self.shift_x = self.key_map_hrztl.get(key, 0)
            self.shift_y = self.key_map_vertl.get(key, 0)

            if self.shift_x or self.shift_y:
                self.shift_blocks(self.shift_x, self.shift_y)
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

    def clear_window(self):
        if system("clear") != 0:
            system("cls")


def main():
    game_2048 = Manager2048()
    game_2048.display_table()
    game_2048.run()


if __name__ == "__main__":
    main()

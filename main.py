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

    def is_valid_position(self, row: int, col: int):
        return (
            (0 <= row < self.max_rows)
            and (0 <= col < self.max_cols)
            and self.grid[row][col] == 0
        )

    def get_block_at(self, row: int, col: int):
        return self.grid[row][col]

    def get_start_stop_step(
        self, shift_x: int, shift_y: int
    ) -> dict[str, tuple[int, int, int]]:
        range_params = {}
        start_row, start_col = 0, 0
        stop_row, stop_col = self.max_rows, self.max_cols
        step_row, step_col = 1, 1
        if shift_y > 0:
            start_row = self.max_rows - 1
            stop_row = -1
            step_row = -1
        print(shift_x)
        if shift_x > 0:
            start_col = self.max_cols - 1
            stop_col = -1
            step_col = -1
        range_params["row"] = (start_row, stop_row, step_row)
        range_params["col"] = (start_col, stop_col, step_col)
        return range_params

    def get_farthest_row(self, shift_y: int, row: int, col: int) -> int:
        new_row = row + shift_y

        if new_row >= self.max_rows or new_row < 0:
            return row
        if self.grid[new_row][col] != 0:
            return row
        return self.get_farthest_row(shift_y, new_row, col)

    def get_farthest_col(self, shift_x: int, row: int, col: int) -> int:
        new_col = col + shift_x

        if new_col >= self.max_cols or new_col < 0:
            return col
        if self.grid[row][new_col] != 0:
            return col
        return self.get_farthest_col(shift_x, row, new_col)

    def handle_merging(self, shift_x: int, shift_y: int, row: int, col: int) -> None:
        if shift_x != 0:
            adjacent_col = col + shift_x
            block = self.grid[row][col]
            if (0 <= adjacent_col < self.max_cols) and block == self.grid[row][
                adjacent_col
            ]:
                self.grid[row][adjacent_col] *= 2
                self.grid[row][col] = 0
        if shift_y != 0:
            adjacent_row = row + shift_y
            block = self.grid[row][col]
            if (0 <= adjacent_row < self.max_rows) and block == self.grid[adjacent_row][
                col
            ]:
                self.grid[adjacent_row][col] *= 2
                self.grid[row][col] = 0

    def shift_blocks(self, shift_x: int, shift_y: int) -> MovementType:
        if shift_x == 0 and shift_y == 0:
            return MovementType.NULL_SHIFT

        blocks_moved = False
        range_params = self.get_start_stop_step(shift_x, shift_y)
        for rowidx in range(*range_params["row"]):
            for colidx in range(*range_params["col"]):
                block = self.grid[rowidx][colidx]
                if block == 0:
                    continue
                new_row = self.get_farthest_row(shift_y, rowidx, colidx)
                new_col = self.get_farthest_col(shift_x, rowidx, colidx)
                if self.is_valid_position(new_row, new_col):
                    self.grid[new_row][new_col] = block
                    self.grid[rowidx][colidx] = 0
                    blocks_moved = True
                self.handle_merging(shift_x, shift_y, new_row, new_col)
        return MovementType.SHIFT_DONE if blocks_moved else MovementType.NO_SLOT

    def handle_input(self):
        key = readchar.readkey()
        self.listen_for_exit(key)

        if not self.isover:
            shift_x = self.key_map_hrztl.get(key, 0)
            shift_y = self.key_map_vertl.get(key, 0)

            if shift_x or shift_y:
                game_state = self.shift_blocks(shift_x, shift_y)
                self.display_table()

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

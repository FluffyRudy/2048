import readchar
from enum import Enum, auto
from os import system
from random import randint, choice, choices
from blockcolors import BLOCK_COLOR, RESET_COLOR

class MovementType(Enum):
    NULL_SHIFT = auto()
    SHIFT_DONE = auto()
    NO_SLOT = auto()


class Manager2048:
    def __init__(self):
        self.grid = generate_init_grid()
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

        cell_width = 4
        line_length = len(self.grid[0]) * (cell_width + 3) + 1
        print(f"\033[1m{'_' * line_length}\033[0m")

        for row in self.grid:
            print("| " + " | ".join(f"{"":^{cell_width}}" for _ in row) + " |")
            row_str = "| " + " | ".join(
                f"{BLOCK_COLOR.get(cell, RESET_COLOR)}{cell if cell != 0 else '':^{cell_width}}{RESET_COLOR}"
                for cell in row
            ) + " |"
            print(row_str)

        print(f"\033[1m{'‾' * line_length}\033[0m")
        print()
        print("Use the arrow keys to move: ↑ ↓ ← →")

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

    def get_empty_pos(self) -> tuple[int, int]:
        empty_positions = []
        for rowindex, rowblock in enumerate(self.grid):
            for colindex, block in enumerate(rowblock):
                if block == 0:
                    empty_positions.append((rowindex, colindex))
        return [-1, -1] if len(empty_positions) == 0 else empty_positions

    def generate_new_block(self) -> dict:
        """keys: [row, col, block]"""
        row, col = choice(self.get_empty_pos())
        block = choices([2, 4, 8], weights=[80, 15, 5])
        if row == -1 or col == -1:
            return {}
        return {"row": row, "col": col, "block": block[0]}

    def assign_new_block(self) -> None:
        new_block_info = self.generate_new_block()
        if new_block_info:
            row = new_block_info["row"]
            col = new_block_info["col"]
            block = new_block_info["block"]
            self.grid[row][col] = block

    def handle_input(self):
        key = readchar.readkey()
        self.listen_for_exit(key)

        if not self.isover:
            shift_x = self.key_map_hrztl.get(key, 0)
            shift_y = self.key_map_vertl.get(key, 0)

            if shift_x or shift_y:
                game_state = self.shift_blocks(shift_x, shift_y)
                if game_state == MovementType.SHIFT_DONE:
                    self.assign_new_block()
                self.display_table()

    def is_game_over(self):
        positions = self.get_empty_pos()
        if len(positions) == 2:
            row, col = positions
            return row == -1 and col == -1
        return False

    def replay(self):
        try:
            if input("play again:(y/n)").lower() == 'y':
                self.grid = generate_init_grid()
            else:
                self.isover = True
        except ValueError:
            print("Invalid choice")

    def has_won(self):
        for blockrow in self.grid:
            for block in blockrow:
                if block == 2048:
                    return True
        return False

    def listen_for_exit(self, key: bytes):
        is_quitting = key == "q"
        if is_quitting:
            self.isover = True
        return self.isover

    def get_board(self) -> list[list[int]]:
        return self.grid

    def set_board(self, board: list[list[int]]):
        self.grid = board

    def get_dimension(self) -> tuple[int, int]:
        return self.max_rows, self.max_cols

    def clear_window(self) -> None:
        if system("clear") != 0:
            system("cls")

    def run(self):
        while not self.isover:
            self.handle_input()
            if self.has_won():
                print("You win")
                self.replay()
            elif self.is_game_over():
                print("game over")
                self.replay()
                self.clear_window()
                self.display_table()



def generate_init_grid():
    NROWS, NCOLS = 4, 4
    grid = [[0 for _ in range(NCOLS)] for _ in range(NROWS)]

    row1, col1 = randint(0, NROWS - 1), randint(0, NCOLS - 1)
    row2, col2 = randint(0, NROWS - 1), randint(0, NCOLS - 1)

    while (row1, col1) == (row2, col2):  
        row2, col2 = randint(0, NROWS - 1), randint(0, NCOLS - 1)

    grid[row1][col1] = choice([2, 4, 8])
    grid[row2][col2] = choice([2, 4, 8])

    return grid


def main():
    game_2048 = Manager2048()
    game_2048.display_table()
    game_2048.run()


if __name__ == "__main__":
    main()

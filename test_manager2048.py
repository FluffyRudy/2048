import unittest
from main import Manager2048


class TestManager2048(unittest.TestCase):

    def setUp(self):
        self.manager = Manager2048()
        self.manager.set_board([[0, 1, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
        self.rows, self.cols = self.manager.get_dimension()

    def test_within_bound(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.manager.get_board()[row][col] == 0:
                    self.assertTrue(self.manager.is_valid_position(row, col))
                else:
                    self.assertFalse(self.manager.is_valid_position(row, col))

    def test_outof_bound(self):
        invalid_positions = [
            (-1, 0),
            (0, -1),
            (self.rows, 0),
            (0, self.cols),
            (-1, -1),
            (self.rows, self.cols),
            (self.rows, -1),
            (-1, self.cols),
        ]
        for row, col in invalid_positions:
            self.assertFalse(self.manager.is_valid_position(row, col))

    def test_occupied_positions(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.manager.get_board()[row][col] != 0:
                    self.assertFalse(self.manager.is_valid_position(row, col))


if __name__ == "__main__":
    unittest.main()

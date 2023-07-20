import unittest
from solver import SodokuSolver
import time


class TestSodokuSolver(unittest.TestCase):
    def test_sudoku_solver(self):
        with open("./tests/hard_sudokus_solved.txt", "r") as f:
            next(f)  # ignore first line as it is the number of sudokus boards
            lines = f.readlines()

        for line in lines:
            puzzle, solution = line.strip().split(",")
            solver = SodokuSolver(puzzle)

            start_time = time.time()
            solver.solve()
            end_time = time.time()
            elapsed_time = end_time - start_time

            solved_puzzle = "".join(
                str(num) for sublist in solver.board for num in sublist
            )

            self.assertEqual(
                solved_puzzle, solution, f"Test failed for puzzle: {puzzle}"
            )
            print(f"Test passed in {elapsed_time} seconds")


if __name__ == "__main__":
    unittest.main()

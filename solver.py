import pprint as pp
import os


class SodokuSolver:
    def __init__(self, board):
        self.board = self.convert_to_matrix(board)

    def convert_to_matrix(self, board):
        # create grid
        matrix = [[0] * 9 for _ in range(9)]

        # populate grid with nine elements
        for i in range(9):
            for j in range(9):
                matrix[i][j] = int(board[9 * i + j])

        # access matrix elements with [y][x]
        return matrix

    def print_board(self):
        # print board as a matrix
        pp.pprint(self.board)

    def fill_cell(self, row, col, number):
        # fill empty cell with number
        self.board[row][col] = number

    def find_empty_cell(self):
        for y in range(9):
            for x in range(9):
                if self.board[y][x] == 0:
                    # print(f"empty cell at ({x}, {y})")
                    return y, x

        print("sodoku solved\n")
        return None

    def solve(self):
        # base case - if no empty cells, then board is solved, this is the goal state
        empty_cell = self.find_empty_cell()

        if not empty_cell:  # if no empty cell is found, the board is solved
            return True
        else:
            row, col = empty_cell

        for choice in range(1, 10):
            if self.is_valid(row, col, choice):
                self.fill_cell(row, col, choice)

                if self.solve():
                    return True

                self.fill_cell(row, col, 0)

        return False

    def is_valid(self, row, col, choice):
        # check row
        for x in range(9):
            if self.board[row][x] == choice:
                return False

        # check column
        for y in range(9):
            if self.board[y][col] == choice:
                return False

        # check box
        box_x = col // 3
        box_y = row // 3

        for y in range(box_y * 3, box_y * 3 + 3):
            for x in range(box_x * 3, box_x * 3 + 3):
                if self.board[y][x] == choice:
                    return False

        return True

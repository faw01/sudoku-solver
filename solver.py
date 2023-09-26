import pprint as pp

class SudokuSolver:
    def __init__(self, board):
        # initialize with the given board and set initial states
        self.board = self.convert_to_matrix(board)
        self.solved = False
        self.stack = []

    def is_solved(self):
        # return if the puzzle is solved
        return self.solved

    def convert_to_matrix(self, board):
        # convert string representation to 2D list (9x9 matrix)
        matrix = [[0] * 9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                matrix[i][j] = int(board[9 * i + j])
        return matrix

    def print_board(self):
        # utility function to print the current board
        pp.pprint(self.board)

    def fill_cell(self, row, col, number):
        # set a number to a specific cell
        self.board[row][col] = number

    def find_empty_cell(self):
        # find the first empty cell in the board; return its position or None if full
        for y in range(9):
            for x in range(9):
                if self.board[y][x] == 0:
                    return y, x
        print("Sudoku Solved!\n")
        return None

    def solve(self):
        # recursively try to fill cells from top-left to bottom-right
        if empty_cell := self.find_empty_cell():
            row, col = empty_cell
        else:
            return True
        for choice in range(1, 10):
            if self.is_valid(row, col, choice):
                self.fill_cell(row, col, choice)
                if self.solve():
                    self.solved = True
                    return True
                self.fill_cell(row, col, 0)
        return False

    def is_valid(self, row, col, choice):
        # check if placing the number violates sudoku rules

        # check the entire row & column
        for i in range(9):
            if self.board[row][i] == choice or self.board[i][col] == choice:
                return False

        # check the 3x3 box
        box_x = col // 3
        box_y = row // 3
        for y in range(box_y * 3, box_y * 3 + 3):
            for x in range(box_x * 3, box_x * 3 + 3):
                if self.board[y][x] == choice:
                    return False
        return True
    
    def solve_step(self):
        # iterative method to solve the sudoku one step at a time
        if not self.stack:
            empty_cell = self.find_empty_cell()
            if not empty_cell:
                self.solved = True
                return False
            row, col = empty_cell
            self.stack.append((row, col, 1))
            num = 1
        else:
            row, col, num = self.stack[-1]

        # try to fill the cell with a number
        for choice in range(num, 10):
            if self.is_valid(row, col, choice):
                self.fill_cell(row, col, choice)
                self.stack[-1] = (row, col, choice + 1)
                if next_cell := self.find_empty_cell():
                    self.stack.append((*next_cell, 1))
                else:
                    self.solved = True
                    self.stack = []
                return True

        self.board[row][col] = 0
        self.stack.pop()
        return True

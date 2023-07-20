import time
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
pygame.font.init()

class Cell:
    def __init__(self, number, x, y, size):
        self.number = number
        self.x = x
        self.y = y
        self.size = size
        self.selected = False

    def draw(self, win):
        font = pygame.font.SysFont("helvetica", 40)
        
        pygame.draw.rect(win, (255, 0, 0) if self.selected else (255, 255, 255), (self.x, self.y, self.size, self.size))
        
        if self.number != 0:  # Only draw number if it's not zero
            text = font.render(str(self.number), 1, (0, 0, 0))
            win.blit(text, (self.x + (self.size // 2 - text.get_width() // 2), 
                            self.y + (self.size // 2 - text.get_height() // 2)))

        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.size, self.size), 1)


class Board:
    def __init__(self, rows, cols, win, cell_size):
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell(0, j * cell_size, i * cell_size, cell_size) 
                       for j in range(cols)] for i in range(rows)]
        self.win = win
        self.cell_size = cell_size
        self.selected = None

    def draw(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(self.win)

    def click(self, pos):
        if pos[0] < self.cell_size * self.rows and pos[1] < self.cell_size * self.cols:
            return (pos[1] // self.cell_size, pos[0] // self.cell_size)
        return None

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False
        self.cells[row][col].selected = True
        self.selected = (row, col)

    def place(self, row, col, num):
        self.cells[row][col].number = num


class Keypad:
    def __init__(self, win, pos, cell_size):
        self.win = win
        self.pos = pos
        self.cell_size = cell_size
        self.cells = [Cell(i+1, pos[0] + (i % 3) * cell_size, pos[1] + (i // 3) * cell_size, cell_size) 
                      for i in range(9)]

    def draw(self):
        for cell in self.cells:
            cell.draw(self.win)

    def click(self, pos):
        if pos[0] >= self.pos[0] and pos[0] < self.pos[0] + self.cell_size * 3:
            if pos[1] >= self.pos[1] and pos[1] < self.pos[1] + self.cell_size * 3:
                return self.cells[((pos[0] - self.pos[0]) // self.cell_size) + 
                                  ((pos[1] - self.pos[1]) // self.cell_size) * 3].number
        return None


def main():
    win = pygame.display.set_mode((966, 645))
    pygame.display.set_caption("Fawdoku")
    board = Board(9, 9, win, 645 // 9)
    keypad = Keypad(win, (645, 0), 645 // 9)
    key = None
    run = True
    start = time.time()
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

                key = keypad.click(pos)
                if key and board.selected:
                    board.place(board.selected[0], board.selected[1], key)
            
        board.draw()
        keypad.draw()
        pygame.display.update()


if __name__ == "__main__":
    print(pygame.font.get_fonts())
    main()
    pygame.quit()

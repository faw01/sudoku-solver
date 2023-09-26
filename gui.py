# hide pygame's welcome message during initialization
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import sys
import random
import time
from solver import SudokuSolver

# custom event for step-by-step solving
SOLVE_STEP_EVENT = pygame.USEREVENT + 1

def initialize_constants():
    global WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_WIDTH, BOARD_SIZE, CELL_SIZE, LINE_WIDTH, THICK_LINE_WIDTH, BORDER_WIDTH, BUTTON_WIDTH
    global WHITE, BLACK, BUTTON_COLOR, BUTTON_HOVER_COLOR, TEXT_COLOR

    pygame.font.init()

    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 540
    BOARD_WIDTH = 540
    BOARD_SIZE = 9 
    CELL_SIZE = BOARD_WIDTH // BOARD_SIZE
    LINE_WIDTH = 1 
    THICK_LINE_WIDTH = 6 
    BORDER_WIDTH = 6 
    BUTTON_WIDTH = WINDOW_WIDTH - BOARD_WIDTH
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BUTTON_COLOR = (100, 100, 100)
    BUTTON_HOVER_COLOR = (150, 150, 150)
    TEXT_COLOR = (255, 255, 255)

def get_random_puzzle(filename="./tests/hard_sudokus.txt"):
    with open(filename, "r") as f:
        lines = f.readlines()

    return random.choice(lines).strip()

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False

    def draw(self, screen):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect)
        font = pygame.font.SysFont('arial', 20)
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            return True
        return False

def draw_board(screen, board, fixed_cells, selected_cell=None):
    for cell in fixed_cells:
        pygame.draw.rect(screen, (220, 220, 220), (cell[0]*CELL_SIZE, cell[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    pygame.draw.rect(screen, BLACK, (0, 0, BOARD_WIDTH, BOARD_WIDTH), BORDER_WIDTH)
    for x in range(0, BOARD_WIDTH, CELL_SIZE):
        if x % (3 * CELL_SIZE) == 0:
            pygame.draw.line(screen, BLACK, (x, 0), (x, BOARD_WIDTH), THICK_LINE_WIDTH)
        else:
            pygame.draw.line(screen, BLACK, (x, 0), (x, BOARD_WIDTH), LINE_WIDTH)
    for y in range(0, BOARD_WIDTH, CELL_SIZE):
        if y % (3 * CELL_SIZE) == 0:
            pygame.draw.line(screen, BLACK, (0, y), (BOARD_WIDTH, y), THICK_LINE_WIDTH)
        else:
            pygame.draw.line(screen, BLACK, (0, y), (BOARD_WIDTH, y), LINE_WIDTH)

    font = pygame.font.SysFont('arial', 40)
    for y, row in enumerate(board):
        for x, num in enumerate(row):
            if num != 0:
                text = font.render(str(num), True, BLACK)
                text_rect = text.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)

    if selected_cell:
        pygame.draw.rect(screen, (255, 0, 0), (selected_cell[0]*CELL_SIZE, selected_cell[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

def initialize_game():
    global initial_puzzle, test_board, fixed_cells, solve_button, solve_step_button, new_puzzle_button, start_time, solved, iterations

    initial_puzzle = get_random_puzzle()
    test_board = [[int(initial_puzzle[BOARD_SIZE * i + j]) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
    fixed_cells = [(x, y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE) if test_board[y][x] != 0]

    solve_button = Button(BOARD_WIDTH + 20, 50, BUTTON_WIDTH - 40, 40, "Solve")
    solve_step_button = Button(BOARD_WIDTH + 20, 100, BUTTON_WIDTH - 40, 40, "Solve Step-by-Step")
    new_puzzle_button = Button(BOARD_WIDTH + 20, 150, BUTTON_WIDTH - 40, 40, "New Puzzle")

    start_time = time.time()
    solved = False
    iterations = 0

def game_loop():
    global initial_puzzle, test_board, fixed_cells, solve_button, solve_step_button, new_puzzle_button, start_time, solved, iterations

    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Sudoku Solver')

    selected_cell = None
    running = True
    elapsed_time = 0

    while running:
        current_time = time.time()
        if not solved:
            elapsed_time = round(current_time - start_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SOLVE_STEP_EVENT:
                if hasattr(solve_step_button, "step_solver"):
                    iterations += 1
                    solve_step_button.step_solver.solve_step()
                    test_board = solve_step_button.step_solver.board
                    if solve_step_button.step_solver.is_solved():
                        solved = True
                        pygame.time.set_timer(SOLVE_STEP_EVENT, 0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_WIDTH:
                        selected_cell = (x // CELL_SIZE, y // CELL_SIZE)
                    else:
                        selected_cell = None
            if event.type == pygame.KEYDOWN and selected_cell:
                if selected_cell not in fixed_cells and not solved:
                    if event.unicode.isdigit() and 0 < int(event.unicode) <= 9:
                        test_board[selected_cell[1]][selected_cell[0]] = int(event.unicode)
                    elif event.key == pygame.K_BACKSPACE:
                        test_board[selected_cell[1]][selected_cell[0]] = 0

            if solve_button.handle_event(event):
                if hasattr(solve_step_button, "step_solver"):
                    solver = solve_step_button.step_solver
                else:
                    solver = SudokuSolver(initial_puzzle)
                solver.solve()
                test_board = solver.board
                solved = True

            if solve_step_button.handle_event(event):
                if not hasattr(solve_step_button, "step_solver"):
                    solve_step_button.step_solver = SudokuSolver(initial_puzzle)
                pygame.time.set_timer(SOLVE_STEP_EVENT, 1)

            if new_puzzle_button.handle_event(event):
                if hasattr(solve_step_button, "step_solver"):
                    delattr(solve_step_button, "step_solver")
                initial_puzzle = get_random_puzzle()
                test_board = [[int(initial_puzzle[BOARD_SIZE * i + j]) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
                fixed_cells = [(x, y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE) if test_board[y][x] != 0]
                start_time = current_time
                solved = False
                iterations = 0

        screen.fill(WHITE)

        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_font = pygame.font.SysFont('arial', 30)
        timer_text = timer_font.render(f"Time: {minutes:02}:{seconds:02}", True, BLACK)
        iterations_text = timer_font.render(f"Iterations: {iterations:,}", True, BLACK)
        screen.blit(timer_text, (BOARD_WIDTH + 20, WINDOW_HEIGHT - 50))
        screen.blit(iterations_text, (BOARD_WIDTH + 20, WINDOW_HEIGHT - 100))

        draw_board(screen, test_board, fixed_cells, selected_cell)
        solve_button.draw(screen)
        solve_step_button.draw(screen)
        new_puzzle_button.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    initialize_constants()
    initialize_game()
    game_loop()
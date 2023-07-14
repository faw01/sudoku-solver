import pprint as pp


def convert_to_grid(board):

    # create grid
    grid = [] * 9

    # populate grid with nine lists
    for i in range(9):
        grid.append([])

        # populate each list with nine elements
        for j in range(9):
            grid[i].append(board[9 * i + j])
    return grid


def print_board(board):
    formatted_grid = convert_to_grid(board)
    pp.pprint(formatted_grid)


if __name__ == "__main__":
    soduko_board = "000075400000000008080190000300001060000000034000068170204000603900000020530200000"
    print_board(soduko_board)
    print()
    solved_board = "693875412145632798782194356357421869816957234429368175274519683968743521531286947"
    print_board(solved_board)

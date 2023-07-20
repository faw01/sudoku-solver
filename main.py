from solver import SodokuSolver

def main():
    # first test case from hard_sudokus_solved.txt
    solver = SodokuSolver(
        "000075400000000008080190000300001060000000034000068170204000603900000020530200000"
    )
    solver.print_board()
    print()
    solver.solve()
    solver.print_board()
    print('answer from hard_sudokus_solved.txt')
    solution = SodokuSolver("693875412145632798782194356357421869816957234429368175274519683968743521531286947")
    solution.print_board()

if __name__ == "__main__":
    main()
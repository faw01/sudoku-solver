def is_valid(board):
    pass


def is_solvable(board):
    pass


def check_board(board):
    # check validity
    validity = is_valid(board)

    # check solvability
    solvability = is_solvable(board)

    # print results
    if validity and solvability == True:
        print("✔ BOARD PASSES ✔")
        return True
    elif validity == True and solvability == False:
        print("✘ BOARD FAILS ✘ - VALID BUT NOT SOLVABLE")
        return False
    elif validity == False and solvability == True:
        print("✘ BOARD FAILS ✘ - SOLVABLE BUT NOT VALID")
        return False
    else:
        print("✘ BOARD FAILS ✘")
        return False

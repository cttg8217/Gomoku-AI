"""
Game Engine For Gomoku
"""

HEIGHT = 8
WIDTH = 8

WHITE = 1
BLACK = -1
EMPTY = 0


def initial_board():
    board = []
    for i in range(HEIGHT):
        board.append([EMPTY] * WIDTH)
    return board


def print_board(board):
    for row in board:
        for cell in row:
            cell_char = ""
            if cell == EMPTY:
                cell_char = "0"
            elif cell == WHITE:
                cell_char = "W"
            elif cell == BLACK:
                cell_char = "B"
            print(cell_char, end=" ")
        print("")


def player(board):
    white_count = 0
    black_count = 0
    for row in board:
        for cell in row:
            if cell == WHITE:
                white_count += 1
            elif cell == BLACK:
                black_count += 1
    if white_count == black_count:
        return WHITE
    if white_count == black_count+1:
        return BLACK

    raise Exception("Unable to Calculate Player: Invalid Board")


def actions(board, interest_range):
    cells_of_interest = []
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if board[row][col] != EMPTY:
                for i in range(row-interest_range, row+interest_range+1):
                    for j in range(col-interest_range, col+interest_range+1):
                        if 0 <= i < HEIGHT and 0 <= j < WIDTH and board[i][j] == EMPTY:
                            if (i, j) not in cells_of_interest:
                                cells_of_interest.append((i, j))

    return cells_of_interest


def execute_action(board, action):
    (row, col) = action
    if board[row][col] != EMPTY:
        raise Exception("Unable to Execute Action: Invalid Action")
    board[row][col] = player(board)


def cancel_last_action(board, action):
    (row, col) = action
    if board[row][col] == EMPTY:
        raise Exception("Unable to Cancel Action: Action Did Not Exit")
    board[row][col] = EMPTY

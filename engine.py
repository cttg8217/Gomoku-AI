"""
Game Engine For Gomoku
"""

height = 8
width = 8

WHITE = 1
BLACK = -1
EMPTY = 0


def initial_board():
    board = []
    for i in range(height):
        board.append([EMPTY] * width)
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
            print(cell)
            if cell == WHITE:
                white_count += 1
            elif cell == BLACK:
                black_count += 1
    print(white_count, black_count)
    if white_count == black_count:
        return WHITE
    if white_count == black_count+1:
        return BLACK
    raise Exception("Unable to Calculate Player: Invalid Board")

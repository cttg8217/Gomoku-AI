from ai import *
from math import inf

board = initial_board()
while True:
    action, value = alpha_beta(board, 4, -inf, inf, 1, True, True)
    execute_action(board, action)
    win = winner(board)
    if win is not None:
        if win == WHITE:
            print("White Wins")
        else:
            print("Black Wins")
        break
    print_board(board)
    row, col = input("input: ").split()
    execute_action(board, (int(row), int(col)))
    win = winner(board)
    if win is not None:
        if win == WHITE:
            print("White Wins")
        else:
            print("Black Wins")
        break

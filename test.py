from engine import *

board = initial_board()

while True:
    print_board(board)
    row = int(input("row: "))
    col = int(input("col: "))
    execute_action(board, (row, col))
    print(evaluate_heuristic(board))

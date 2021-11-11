from engine import *

board = initial_board()

while True:
    print_board(board)
    row = int(input("row: "))
    col = int(input("col: "))
    execute_action(board, (row, col))
    open_count, closed_count = total_threat_count(board, WHITE)
    print(open_count, closed_count)

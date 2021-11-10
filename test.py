from engine import *

board = initial_board()
board[0][0] = WHITE
board[1][1] = BLACK
print(actions(board, 1))

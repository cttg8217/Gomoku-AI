from ai import *
from math import inf

board = initial_board()
print(alpha_beta(board, 5, -inf, inf, 1, True, True))

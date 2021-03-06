"""
Game Engine For Gomoku
"""
from math import inf, isinf
from functools import lru_cache

HEIGHT = 9
WIDTH = 9

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
                cell_char = "\033[33m" + 'O' + '\033[0m'
            elif cell == WHITE:
                cell_char = "\033[97m" + 'W' + '\033[0m'
            elif cell == BLACK:
                cell_char = "\033[30m" + 'B' + '\033[0m'
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
    if len(cells_of_interest) == 0:
        cells_of_interest.append((HEIGHT//2, WIDTH//2))

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


def threat_search(board, beginning, delta_row, delta_col, color):
    (row, col) = beginning
    open_count = {2: 0, 3: 0, 4: 0, 5: 0}
    closed_count = {2: 0, 3: 0, 4: 0, 5: 0}
    status = 1
    count = 0
    while 0 <= row < HEIGHT and 0 <= col < WIDTH:
        if board[row][col] == color:
            count += 1
        elif board[row][col] == EMPTY:
            if 2 <= count <= 5:
                if status == 2:
                    open_count[count] += 1
                elif status == 1:
                    closed_count[count] += 1
            status = 2
            count = 0
        else:
            if 2 <= count <= 5:
                status -= 1
                if status == 1:
                    closed_count[count] += 1
            status = 1
            count = 0
        row += delta_row
        col += delta_col
    if 2 <= count <= 5:
        status -= 1
        if status == 1:
            closed_count[count] += 1
    return open_count, closed_count


def total_threat_count(board, color):
    total_open_count = {2: 0, 3: 0, 4: 0, 5: 0}
    total_closed_count = {2: 0, 3: 0, 4: 0, 5: 0}
    for row in range(HEIGHT):
        open_count, closed_count = threat_search(board, (row, 0), 0, 1, color)
        for i in range(2, 6):
            total_open_count[i] += open_count[i]
            total_closed_count[i] += closed_count[i]

    for col in range(WIDTH):
        open_count, closed_count = threat_search(board, (0, col), 1, 0, color)
        for i in range(2, 6):
            total_open_count[i] += open_count[i]
            total_closed_count[i] += closed_count[i]

    for row in range(HEIGHT):
        open_count, closed_count = threat_search(board, (row, 0), 1, 1, color)
        for i in range(2, 6):
            total_open_count[i] += open_count[i]
            total_closed_count[i] += closed_count[i]

    for col in range(1, WIDTH):
        open_count, closed_count = threat_search(board, (0, col), 1, 1, color)
        for i in range(2, 6):
            total_open_count[i] += open_count[i]
            total_closed_count[i] += closed_count[i]

    for row in range(HEIGHT):
        open_count, closed_count = threat_search(board, (row, 0), -1, 1, color)
        for i in range(2, 6):
            total_open_count[i] += open_count[i]
            total_closed_count[i] += closed_count[i]

    for col in range(1, WIDTH):
        open_count, closed_count = threat_search(board, (HEIGHT-1, col), -1, 1, color)
        for i in range(2, 6):
            total_open_count[i] += open_count[i]
            total_closed_count[i] += closed_count[i]

    return total_open_count, total_closed_count


@lru_cache(maxsize=1000)
def evaluate_heuristic(board):
    white_open_threats, white_closed_threats = total_threat_count(board, WHITE)
    black_open_threats, black_closed_threats = total_threat_count(board, BLACK)
    if white_open_threats[5] + white_closed_threats[5] > 0:
        return inf
    if black_open_threats[5] + black_closed_threats[5] > 0:
        return -inf
    h = 4800*(white_open_threats[4] - black_open_threats[4])
    h += 500*(white_closed_threats[4] - black_closed_threats[4])
    h += 500*(white_open_threats[3] - black_open_threats[3])
    h += 200*(white_closed_threats[3] - black_closed_threats[3])
    h += 50*(white_open_threats[2] - black_open_threats[2])
    h += 10*(white_closed_threats[2] - black_closed_threats[2])
    return h


def winner(board):
    h = evaluate_heuristic(tuple(map(tuple, board)))
    if isinf(h):
        if h > 0:
            return WHITE
        else:
            return BLACK
    return None

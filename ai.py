from engine import *
from math import inf, isinf


def alpha_beta(board, depth, alpha, beta, interest_range, maximizing_player, return_action):
    h = evaluate_heuristic(tuple(map(tuple, board)))
    if depth == 0 or isinf(h):
        return h

    if maximizing_player:
        value = -inf
        optimal_action = None
        for action in actions(board, interest_range):
            execute_action(board, action)
            local_min = alpha_beta(board, depth-1, alpha, beta, interest_range, False, False)
            if value < local_min:
                value = local_min
                optimal_action = action
            cancel_last_action(board, action)
            if value > beta:
                break
            alpha = max(alpha, value)
        if return_action:
            return optimal_action, value
        return value

    else:
        value = inf
        optimal_action = None
        for action in actions(board, interest_range):
            execute_action(board, action)
            local_max = alpha_beta(board, depth-1, alpha, beta, interest_range, True, False)
            if local_max < value:
                value = local_max
                optimal_action = action
            cancel_last_action(board, action)
            if value < alpha:
                break
            beta = min(beta, value)
        if return_action:
            return optimal_action, value
        return value

"""
Tic Tac Toe Player
"""

import sys
import math
import copy

X = "X"
O = "O"
EMPTY = None
EMPTY_BOARD = [[EMPTY, EMPTY, EMPTY],
               [EMPTY, EMPTY, EMPTY],
               [EMPTY, EMPTY, EMPTY]]
ALL_ACTIONS = {
    (0, 0), (0, 1), (0, 2), 
    (1, 0), (1, 1), (1, 2),
    (2, 0), (2, 1), (2, 2)
}
INFINITE = 1000000


def initial_state():
    """
    Returns starting state of the board.
    """
    return EMPTY_BOARD


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == EMPTY_BOARD:
        return X
    else:
        x_moves = 0
        o_moves = 0
        for r in board:
            for move in r:
                x_moves = x_moves + 1 if move == X else x_moves
                o_moves = o_moves + 1 if move == O else o_moves
        return X if x_moves == o_moves else O


def winner(board):
    """
    Returns the winner of the game, if there is one. None otherwise.
    """
    class PlayerResults:
        def __init__(self, player):
            self.player = player
            self.rows_count = [0, 0, 0]
            self.cols_count = [0, 0, 0]
            self.p_diag_count = 0
            self.s_diag_count = 0

        def increment_at(self, r, c):
            self.rows_count[r] = self.rows_count[r] + 1
            self.cols_count[c] = self.cols_count[c] + 1
            if r == c:
                self.p_diag_count = self.p_diag_count + 1
            if r + c == 2:
                self.s_diag_count = self.s_diag_count + 1

        def will_win_with_increment_at(self, r, c):
            return self.rows_count[r] + 1 == 3 \
                or self.cols_count[c] + 1 == 3 \
                or (r == c and self.p_diag_count + 1 == 3) \
                or (r + c == 2 and self.s_diag_count + 1 == 3)

    if board == EMPTY_BOARD:
        return None

    x_resutls = PlayerResults(X)
    o_resutls = PlayerResults(O)

    for r, col in enumerate(board):
        for c, move in enumerate(col):
            if move == X:
                if x_resutls.will_win_with_increment_at(r, c):
                    return X
                x_resutls.increment_at(r, c)

            if move == O:
                if o_resutls.will_win_with_increment_at(r, c):
                    return O
                o_resutls.increment_at(r, c)

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # the board is terminal if there is a winner or there are no more non EMPTY cells
    available_cells = [cell for row in board for cell in row if cell == EMPTY]
    return len(available_cells) == 0 or bool(winner(board))


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # returns empty set if terminal status
    if board == EMPTY_BOARD:
        return ALL_ACTIONS

    if terminal(board):
        return set()
    
    result = set()
    for r, col in enumerate(board):
        for c, move in enumerate(col):
            if move == EMPTY:
                result.add((r, c))
    return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # returns same board if terminal status
    if terminal(board):
        return board

    if action not in actions(board):
        raise ValueError('Invalid Action')

    row, col = action
    current_palyer = player(board)
    result = copy.deepcopy(board)
    result[row][col] = current_palyer
    return result


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    who_wins = winner(board)
    if who_wins == X:
        return 1
    elif who_wins == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def max_value(board_state, min_so_far):
        if terminal(board_state):
            return utility(board_state)

        v = -INFINITE
        for action in actions(board_state):
            next_min = min_value(result(board_state, action), v)
            v = max(v, next_min)
            if next_min > min_so_far:
                # existing the loop now as this maximising branch won't allow the minimising score to go below min_so_far
                break
        return v

    def min_value(board_state, max_so_far):
        if terminal(board_state):
            return utility(board_state)
        
        v = INFINITE
        for action in actions(board_state):
            next_max = max_value(result(board_state, action), v)
            v = min(v, next_max)
            if next_max < max_so_far:
                # existing the loop now as this minimising branch won't allow the maximising score to go above max_so_far
                break
        return v

    if terminal(board):
        return None

    current_player = player(board)
    possible_actions = actions(board)

    best_action = None
    best_score = -INFINITE if current_player == X else INFINITE

    for action in possible_actions:
        # this makes sure that if any move brings to immediate win is favourited even if others have high score
        if board != EMPTY_BOARD and winner(result(board, action)) == current_player:
            return action

        if current_player == X:
            # maximisign player
            new_action_score = min_value(result(board, action), -INFINITE)
            if new_action_score > best_score:
                best_score = new_action_score
                best_action = action
        if current_player == O:
            # minimising player
            new_action_score = max_value(result(board, action), INFINITE)
            if new_action_score < best_score:
                best_score = new_action_score
                best_action = action

    return best_action
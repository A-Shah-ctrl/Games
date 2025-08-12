"""
Tic Tac Toe Player

"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == [[EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]:
        return X
    else:
        x_ = 0
        o_ = 0
        for i in range(0,3):
            x_ += board[i].count(X)
            o_ += board[i].count(O)
        if o_ < x_:
            return O
        else:
            return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    act = []
    for i in range(3):
        if board[i][0] == EMPTY:
            act.append((i,0))
        if board[i][1] == EMPTY:
            act.append((i,1))
        if board[i][2] == EMPTY:
            act.append((i,2))
    return act

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    copy_board = copy.deepcopy(board)
    #Finds if 'X' needs to be put or 'O'
    turn = player(board)
    row = action[0]
    column = action[1]
    if row > 2 or row < 0 or column > 2 or column < 0:
        raise Exception
    #Assigns it to the position
    copy_board[row][column] = turn
    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    value = utility(board)
    if value == 1:
        return X
    elif value == 0:
        return "No one"
    return O

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Diagonal Win
    if board[0][0] == board[1][1] == board[2][2] == X or board[0][2] == \
            board[1][1] == board[2][0] == X or \
            board[0][0] == board[1][1] == board[2][2] == O or board[0][2] == \
            board[1][1] == board[2][0] == O:
        return True

    full = 0
    for i in range(0, 3):
        # Horizontal win
        if board[i].count(X) == 3 or board[i].count(O) == 3:
            return True
        # Vertical Win
        elif board[0][i] == board[1][i] == board[2][i] == X or \
                board[0][i] == board[1][i] == board[2][i] == O:
            return True
        else:
            full += board[i].count(X) + board[i].count(O)
            if full == 9:
                return True

    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    for i in range(0, 3):
        # Horizontal win
        if board[i].count(X) == 3:
            return 1
        elif board[i].count(O) == 3:
            return -1
        # Vertical Win
        elif board[0][i] == board[1][i] == board[2][i] == X:
            return 1
        elif board[0][i] == board[1][i] == board[2][i] == O:
            return -1

    # Diagonal Win
    if board[0][0] == board[1][1] == board[2][2] or board[0][2] == \
            board[1][1] == board[2][0]:
        if board[1][1] == X:
            return 1
        else:
            return -1
    return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        possible_acts = actions(board)
        if player(board) == X:
            value = -2
            act = None
            for action in possible_acts:
                curr_val = _minimum(board,action)
                if curr_val > value:
                    act = action
                    value = curr_val
                    if value == 1:
                        break
            return act

        elif player(board) == O:
            value = 2
            act = None
            for action in possible_acts:
                curr_val = _maximum(board,action)
                if curr_val < value:
                    act = action
                    value = curr_val
                    if value == -1:
                        break
            return act

def _maximum(board, action) -> int:
    new_board = result(board, action)
    if terminal(new_board):
        return utility(new_board)
    acts = actions(new_board)
    v = -2
    for a in acts:
        v = max(v,_minimum(new_board, a))
        if v == 1:
            break
    return v


def _minimum(board, action) -> int:
    new_board = result(board, action)
    if terminal(new_board):
        return utility(new_board)
    acts = actions(new_board)
    v = 2
    for a in acts:
        v = min(v, _maximum(new_board, a))
        if v == -1:
            break
    return v





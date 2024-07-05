"""
Tic Tac Toe Player
"""

import copy
import math

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
    xMoves = 0
    oMoves = 0

    for row in board:
        for item in row:
            if item == X:
                xMoves += 1
            if item == O:
                oMoves += 1
    
    if xMoves <= oMoves:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActions = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possibleActions.add((i, j))

    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise "Invalid move: Cell is not empty"
    
    if action[0] < 0 or action[0] > len(board):
        raise "Invalid move: Out of range"
    
    if action[1] < 0 or action[1] > len(board[action[0]]):
        raise "Invalid move: Out of range"
    
    newBoard = copy.deepcopy(board)

    newBoard[action[0]][action[1]] = player(newBoard)
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows for a win
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]

    # Check columns for a win
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not EMPTY:
            return board[0][col]

    # Check diagonals for a win
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    # No winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    
    for row in board:
        for item in row:
            if item == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    currentWinner = winner(board)

    if currentWinner == O:
        return -1
    
    if currentWinner == X:
        return 1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None
    
    currentPlayer = player(board)
    
    if currentPlayer == X:
        v = float('-inf')
        best_action = None
        for action in actions(board):
            min_val = minValue(result(board, action))
            if min_val > v:
                v = min_val
                best_action = action
        return best_action
    
    if currentPlayer == O:
        v = float('inf')
        best_action = None
        for action in actions(board):
            max_val = maxValue(result(board, action))
            if max_val < v:
                v = max_val
                best_action = action
        return best_action

    return None


def maxValue(board):
    if terminal(board):
        return utility(board)
    
    v = float('-inf')

    for action in actions(board):
        v = max(v, minValue(result(board, action)))

    return v


def minValue(board):
    if terminal(board):
        return utility(board)
    
    v = float('inf')

    for action in actions(board):
        v = min(v, maxValue(result(board, action)))
    
    return v
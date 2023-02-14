
from copy import deepcopy
from utils import cook_status, is_quarto, try_easy_win, avoid_easy_defeat

import numpy as np

DEBUG = True


def minmax_place(curr_state: tuple,  # (board, given_piece) move is where to place the piece given
            is_maximizing: bool, 
            depth: int,
            alpha=-1, 
            beta=1):

    if DEBUG: print("PL DEPTH: ", depth)

    # INIT
    board = curr_state[0]
    given_piece = curr_state[1]

    # The score is either 1 or -1, so the simulation ended
    # and we are in a leaf
    scr = score(board=board, is_maximizing= is_maximizing) 
    
    if depth == 0 or scr != 0:

        if DEBUG and depth == 0:
            print("PL___DEPTH LIMIT REACHED")
        return scr if depth > 0 else 0


    if is_maximizing:
        # ALl possile states from curr_state
        possible_new_states = cook_status(board=board,
                                          selected_piece=given_piece)["possible_new_states"]

        # Check best Placing
        max_eval = -100_000
        for state, move in possible_new_states:
           
            # I Choose my opponent's piece
            eval = minmax_choice(board=deepcopy(state), 
                                depth=depth -1, 
                                is_maximizing=True,
                                alpha=alpha,
                                beta=beta)
            
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)

            if beta <= alpha:
                if DEBUG: print("Break")
                break
       
        return max_eval

    else:

        possible_new_states = cook_status(board=board,
                               selected_piece=given_piece)["possible_new_states"]
        min_eval = 100_000
        for state, move in possible_new_states:

            eval = minmax_choice(board= deepcopy(state),
                                depth= depth -1,
                                is_maximizing=False)
            
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)  

            if beta <= alpha:
                if DEBUG: print("Break")
                break

        return min_eval

def minmax_choice(board: np.ndarray,  # (board, given_piece) move is where to place the piece given
            is_maximizing: bool, 
            depth: int,
            alpha=-1, 
            beta=1):

    if DEBUG: print("CH DEPTH: ", depth)
    # The score is either 1 or -1, so the simulation ended
    # and we are in a leaf
    scr = score(board=board, is_maximizing= is_maximizing) 
    if depth == 0 or scr != 0:

        if DEBUG and depth == 0:
            print("CH___DEPTH LIMIT REACHED")
        return scr if depth > 0 else 0

    if is_maximizing:
        possible_pieces = cook_status(board=board, 
                                      choosing=True)["possible_pieces"]
        max_eval = -100_000
        for piece in possible_pieces:
            eval = minmax_place(curr_state=(deepcopy(board), piece),
                                depth= depth -1,
                                is_maximizing=False)

            max_eval = max(max_eval, eval)
            beta = max(beta, eval)

            if beta <= alpha:
                if DEBUG: print("Break")
                break

        return max_eval

    else:

        possible_pieces = cook_status(board=board, 
                                      choosing=True)["possible_pieces"]

        # Check best Placing
        min_eval = 100_000
        for piece in possible_pieces:
            eval = minmax_place(curr_state= (deepcopy(board), piece), 
                                depth= depth -1, 
                                is_maximizing=True,
                                alpha=alpha,
                                beta=beta)

            min_eval = min(min_eval, eval)
            beta = min(beta, eval)

            if beta <= alpha:
                if DEBUG: print("Break")
                break
       
        return min_eval


def score(board, is_maximizing):
    """
    see returns

    Args:
        state (quarto.Quarto): check the board

    Returns:
        int: 1 if the player placed the last piece, 
            -1 if the opponent placed the last piece,
             0 if the game is not ended yet/ draw
    """

    if is_quarto(board):
        return 1 if is_maximizing else -1
    return 0

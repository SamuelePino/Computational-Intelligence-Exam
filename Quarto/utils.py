# Utils functions used by Players

from collections import deque
import quarto
import random
from copy import deepcopy
import numpy as np

def cook_status(board = None, 
                choosing = False, 
                minmax = False,
                selected_piece: int = None,
                my_test = False,
                shuffle = False) -> dict:

    

    cooked = dict()
    
    if choosing:
        pieces = [i for i in range(0, 15 + 1)]
        for i in range(4):
            for j in range(4):
                if (board[i][j] >= 0): # there is a piece
                   
                    try:
                      pieces.remove(board[i][j])
                    except:
                        raise ValueError(f"Board:\n{board}\n\nPiece {board[i,j]}")

        cooked['possible_pieces'] = pieces
        if shuffle:
            random.shuffle(cooked['possible_pieces'])

    else:

        if my_test:
        
            # (Possible New State, (y,x))
            cooked['future_states'] = []
            if not minmax:
                for y in range(4):
                    for x in range(4):
                        if board[y][x] < 0:
                            temp_board = deepcopy(board)

                            #Temp update of the board:
                            temp_board[y][x] = selected_piece
                            cooked['future_states'].append((temp_board, (x,y)))  
                if shuffle:
                    random.shuffle(cooked['future_states'])

        # Role: Positioning of a Piece
        else:
            # (Possible New State, (y,x))
            cooked['possible_new_states'] = []
            for y in range(0, 3 + 1):
                for x in range(0, 3 + 1):
                    #if board[y][x] == -1:
                    if not (y < 0 or x < 0 or x > 3 or y > 3 or board[y, x] >= 0):
                        temp_board = deepcopy(board)

                        #Temp update of the board:
                        temp_board[y, x] = selected_piece
                        cooked['possible_new_states'].append((temp_board, (x,y)))  
            if shuffle:
                    random.shuffle(cooked['possible_new_states'])
        if minmax:
            #format: (y,x, piece)  
            # Given a piece, saves
            # where it can e placed (y,x) 
            # and what piece is it (piece)
            # contains all possible placing for it
            cooked['legal_moves'] = [(y,x) for y in range(4) for x in range(4) if board[y][x] < 0]

            if shuffle:
                random.shuffle(cooked['legal_moves'])
                

    return cooked

def check_list(l: list) -> int:
    """
    check if the given list is full and if it contains 
    a set of 4 elements sharing at least an attribute

    Args:
        l (list): _description_

    Returns:
        int: a number greater than 0 if the list is full (no -1) and 
        if the list contains all pieces sharing at least an attribute
    """
 
    #Check if it has empty places
    for elem in l:
        if elem < 0:
            return False

    bits_matrix = ['{:04b}'.format(elem) for elem in l]

    no_bit_shared = True
    for col in range(4):
        
        column = [bits_matrix[row][col] for row in range(4)]
        # if all elem in the column are equal to the first
        no_bit_shared =  not all([i == column[0] for i in column])

        if not no_bit_shared:   # if there exist a column with all 1 or 0
            return True
 
def is_quarto(board: np.ndarray):
    """Using XOR and check if the Xor is greater than 1 to see if 

    Args:
        board (np.ndarray): _description_

    Returns:
        _type_: _description_
    """
    # check each row
    for row in board:   
        if check_list(row):
            return  True

    # check each col
    for col in board.transpose():        
        if  check_list(col):
            return  True

    #  main Diag
    if  check_list(board.diagonal()):
        return  True
    #  Anti Diag
    if  check_list(np.rot90(board).diagonal()):
        return  True

    # If none of the above check works, then
    return False

if __name__ == '__main__':
    q = quarto.Quarto()
    print(q.get_board_status())

    q = np.array([[-1, -1, -1, 7],
                    [-1, 6, -1, -1],
                    [-1, -1, -1, -1],
                    [-1, -1,  5, -1]])

    cooked_stats = cook_status(board=q ,#q.get_board_status(), 
                               selected_piece= 5)["possible_new_states"]
    for i in cooked_stats:
        print(i, '\n')


def try_easy_win(possible_new_states) -> tuple:
    """
    It returns a winning move if there exist one, otherwise it will return a random move and a flag

    Args:
        board (np.ndarray): _description_
        possible_new_states (_type_): _description_

    Returns:
        (move, is_winning): return the move and if is winning or random
    """
    for board_state, move in possible_new_states:
        if is_quarto(board_state):
            return  ((move[0],move[1]), True)  

    else:
        return ((move[0],move[1]), False)   # Use the last available move checked


def avoid_easy_defeat(board, possible_pieces) -> tuple:
    """
    It check if there exist a piece which won't let the opponent win
    and return it, otherwise it will return a random piece

    Args:
        board (_type_): _description_
        bool (_type_): _description_

    Returns:
        (piece, is_winning): return the piece choosen and if it will let the opponent win or not
    """

    # For each piece possible
    for piece in possible_pieces:
        
        # We get all possible state, starting with that piece
        possible_new_states = cook_status(board=board, 
                                          selected_piece=piece)["possible_new_states"]
        
        no_safe_pieces = False
        # Then we check for each state with this piece, 
        # if there exist one which is winning (for the opponent)
        for board_state, move in possible_new_states:

            # if it  is a winning state for the opponent 
            # we can lose... so let's try another piece
            # leaving this for
            if is_quarto(board=board_state):
                no_safe_pieces = True
                break

        #if istead this piece is safe, let's play it
        if not no_safe_pieces:
            # Giving a piece with which we won't lose
            return (piece, False)

    # If there is no safe piece, we play the last
    return (random.choice(possible_pieces), True)

def get_num_similarities(p1, p2) -> int:
    ...

def get_simm_equivalence(board) -> tuple:

    """two state equivalent if both of them had in order:
   - The same number of pieces
   - The pieces configuration which differs only for rotation and/or flips
   - The same graph of similarities of the pieces
    
   #Draft of PseudoCode ... 
    1) Check b1.num_pezzi = b_ref[i].num_pezzi for ogni b_ref che abbiamo
        pezzi della board in analisi usati come indice per cercare nella lista di 
        b_ref con quel numero di pezzi

        N = b1.num_pezzi
        list_b_ref_with_N_pieces = simm[N] (un dict)

    2) se 1) è ok:
        Check se esiste una trasf in simmetries che porta b1 a 
            coincedere con una delle b_ref con N pezzi
    for b_ref in b_refs:
        for t in simmetries:
            if t(b1) == b_ref:
                ...
    3) se 2) è ok: 
        controlla che le relazioni tra i pezzi siano le stesse

    for ogni coppia di pezzi su ogni riga, ogni col, ogni diag, ogni adiag:
        if not get_num_similarities(b1) == get_num_similarities(b_ref):
            return NON-EQUIVALENTI

    """      
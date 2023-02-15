from copy import deepcopy
import random
from utils import cook_status
from dataclasses import dataclass
from utils import cook_status, is_quarto
from dataclasses import dataclass
import logging

import numpy as np

logging.getLogger().setLevel("DEBUG")

ME = True
OPPONENT = False

@dataclass
class MinMaxNode():
    board: np.ndarray #board containing the move already taken

    choosen_piece: int # Piece choosen for the opponent    
                        # may be on 4 bit to avoid wasting mem

    player: bool   #False is opponent's turn

    children: list #All possible state starting from this state
    
    # So every combination of where the choosen_piece has been placed on the 
    # Board and what piece among remaining ones has been chosen to be
    # passed to the opponent

    def get_legal_moves(self):
        """
        Return a list with all possible moves for the possile pieces given

        Returns:
            list  : list with all possible moves for all possile pieces given
        """
        # Given the self.choosen_piece, let's find all possible moves
        # for the opponent, using the same piece      
        lm = [(y,x) for y in range(4) for x in range(4) if self.board[y][x] < 0]  
    
        return lm

    def make_opp_move(self, move: tuple):
        """
        Creates all possible state starting from this current state (where it is called).
        Each new state (child) will have the board with the 'move' taken, and one of all
        possible pieces as choosen piece for the other player

        Args:
            move (tuple): Move taken with self.choosen_piece
        """

        # Move is: Where to place what piece
        new_board = deepcopy(self.board)
        
        y = move[0]
        x = move[1]
        piece_to_place = self.choosen_piece

        #logging.debug("--Before",new_board, piece_to_place, self.choosen_piece)
        #This is the new board, updated with the last move 
        new_board[y][x] = piece_to_place
        #logging.debug("--After",new_board, piece_to_place, self.choosen_piece)
        
        poss_pieces = cook_status(board=new_board, 
                                  choosing=True,
                                  shuffle=True)['possible_pieces']
        
        self.children = [] #re-init children for this move
        #Then we create all possible children where the move is taken
        # ad we loop over all possible (move-piece) combs
        
        logging.debug("\tPoss-Pieces: ", poss_pieces)
        self.children = [MinMaxNode(board=new_board, 
                              choosen_piece=p,
                              player= not self.player,
                              children=[])\

                        for p in poss_pieces]
       

    def evaluate(self):
        """
        see returns

        Args:
            state (quarto.Quarto): check the board

        Returns:
            int: 1 if the player placed the last piece, 
                -1 if the opponent placed the last piece,
                    0 if the game is not ended yet
        """
        if is_quarto(self.board):
            #1 if it's ME -1 if it's OPPONENT
            return 10 if self.player else -10
        return 0

    def is_game_over(self):
        # If someone won, or there is a draw
        return (is_quarto(self.board) or np.all([i != -1 for i in self.board]))

def minimax(state: MinMaxNode, depth, alpha, beta, maximizing_player):
    
    logging.debug(f"{'    MAX' if maximizing_player else 'MIN'}:  DEPTH- {depth}")
    #Termination
    
    if depth == 0 or state.is_game_over():
        #1 if it's ME 
        # -1 if it's OPPONENT
        # 0 if draw
        return state.evaluate()
        
    logging.debug("\tTERMINATION NOT REACHED")

    if maximizing_player:
        value = 1000
        # given the choosen piece of the state
        # let's explore every possible future state starting from:
        for move in state.get_legal_moves():
            # simulate if the opponent has taken this move
            # placing the choosen_piece of the state
            state.make_opp_move(move) #update children of this state for this opp move
            for next_state in state.children:

                logging.debug("\tLET's DIVE IN", depth-1)
                value = min(value, minimax(next_state, depth - 1, alpha, beta, False))
                beta = min(beta, value)
                logging.debug(f"\tMAX:  |Depth: {depth} |Value: {value} |alpha {alpha}  |beta {beta}")

                if alpha >= beta: 
                    return value

        return value

    else:
        value = -1000
        for move in state.get_legal_moves():
            state.make_opp_move(move)
            for next_state in state.children:
                logging.debug("MIN: LET's DIVE IN", depth-1)
                value = max(value, minimax(next_state, depth - 1, alpha, beta, True))
                alpha = max(alpha, value)
                logging.debug(f"MIN:  |Depth: {depth} |Value: {value} |alpha: {alpha} |beta: {beta}")

                if alpha >= beta: 
                     return value

        return value


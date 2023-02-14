# Computational-Intelligence-Exam

# Final Project: Making a Quarto Player

--> [Repo Links](https://github.com/SamuelePino/Computational-Intelligence-Exam)


## What is Quarto
brief intro, rule etc

## Getting Informed

I studied the maths behind Quarto, in order to understand its true complexity and how exploits som sort of symmetries etc. A crucial site was [this page](https://stmorse.github.io/journal/quarto-part1.html) where I truly understand how many states could exist in end game (~21 10e12). In Materials there are other links I used to analyze the problem

## The Journey

Given this complexity and my computational constraints I discussed with my colleague about the best approach. He decided to use Reinforcement Learning, whilst I focused on MinMax.

The RL approach turned out to be unfeasible considering our resources, due to the gargantuan dictionaries needed for the state-value tables, and the huge number of collisions which derive from such enormous tables. 

I decided to exploit a MinMax algorithm to approach this game. 

### - Double Min Max
At first I tried directly my own ideas, such as using two trees, one for choosing the best position for the given piece, the other one for choosing the best piece to give to the opponent. 
There are two functions, one for choosing where to place a given piece (`minmax_place`), and one to choose the best piece to give the opponent a hard time (`minmax_choice`).

The first:
```py
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

```

The latter:

```py
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
```
These functions are used in the main function of the `DoubleMinMax_player`, an object made like:

```py

class DoubleMinMax(quarto.Player):
    def __init__(self, quarto: quarto) -> None:
        """
        The player starts playing randomly, then at a specific point
        it starts to play using minmax.
        This should limit the amount of states to analyse, especially at the beginning

        Args:
            quarto (quarto): pass the game
        """

        super().__init__(quarto)
        self._play_random: bool = True
        self._turns_played_rnd: int = 0
        self._MAX_RND = 2
        self._MAX_DEPTH = 30
```
where there are settable parameters such asthe number of turns played randomly, the max_depth reachable ...
The main methods used are:

```py
def choose_piece(self) -> int:

        game = self.get_game()
        board = game.get_board_status()
        possible_pieces = cook_status(board=board,
                                      choosing=True)["possible_pieces"]

        candidate_piece, is_winning = avoid_easy_defeat(board, possible_pieces)

        # if is winning is True, there is no hope for us, unless the opponent plays randomly
        # so it can be useful immplement 'or is_winninng' in the following if-statement, 
        # and die with honor
        if self._play_random or is_winning: 
            print("RANDOM PLAY CH", candidate_piece)
            return candidate_piece

        for piece in possible_pieces:

            score = minmax_place(curr_state=(deepcopy(board), piece), 
                                is_maximizing=False, # it's up to the opponent to place
                                depth=self._MAX_DEPTH,
                                alpha=-100_000,
                                beta=100_000)

            # if we find a state in which we win when we choose this piece...
            if score > 0:   
                print("Found a choosing to WIN", piece)
                return piece
        
        print("Choose NADA ...", candidate_piece)
        return candidate_piece



            
    def place_piece(self) -> tuple((int, int)):

        game = self.get_game()
        board = game.get_board_status()
        piece_to_place = game.get_selected_piece()
        possible_new_states = cook_status(board=board,
                                          selected_piece=piece_to_place)["possible_new_states"]

        # check for stopping playing random
        self._play_random = False if self._turns_played_rnd >= self._MAX_RND else True

        candidate_move, is_winning  = try_easy_win(possible_new_states)

        if is_winning or self._play_random:
            self._turns_played_rnd += 1
            print("RANDOM PLAY PL", candidate_move)
            return candidate_move # (y,x) ??
        
        # Else MinMax
        for state, move in possible_new_states:

            score = minmax_choice(board=deepcopy(state), 
                                  is_maximizing=True, 
                                  depth=self._MAX_DEPTH,
                                  alpha=-100_000,
                                  beta=100_000)

            if score > 0:
               print("Found a placing to WIN", (move[1], move[0]) )
               return (move[1], move[0])
        
        print("Place NADA ...", candidate_move)
        return candidate_move
```
These methods explore  all possible states and use minmax to find the best move or the best piece to give.

In both functions the value `is_maximizing` is not fixed in this code here, because there were some bugs I didn't analyzed deeply, probably linked to these values too. 
This strategy seemed to not working out, so I considered the entire approach wrong.

### - Single Min Max
I decided to use a single tree approach, but I have a hard time developing a good general state (node) which could condensate both the decision of where to place the piece, and what piece to give to the opponent. 
I search online different inspirations.
I found a Java Implementation of this agent and I tried to understand his ideas.
The state used was a single object containing the board state, with the placement already made, and the piece ready for the opponent on next turn. 
I implemented it as a dataclass with the needed values in it.

```py

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
```
Here each state/node is a dataclass object containing the `board` already modified by the move taken by the current player, the `choosen_piece` for  the opponent, the current `player` and the list of the `children` of this node, which are all possible states obtainable starting from this current node.

The main function is:

```py
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
```

The main class of the `SingleMinMax_Player` has some crucial parameters used for setting max depth and the number of turns played randomly: 

```py
class SingleMinMax(quarto.Player):
    def __init__(self, quarto: quarto) -> None:
        """
        The player starts plaing randomly, then at a specific point
        it starts to play using minmax.
        This should limit the amount of states to analyse

        Args:
            quarto (quarto): pass the game
            max_depth (int): max exploration depth in the tree
            pieces_left (int): number of pieces left to activate minmax
        """

        super().__init__(quarto)
        self._play_random: bool = True
        self._turns_played_rnd: int = 0
        self._MAX_RND = 2
        self._MAX_DEPTH = 3
        self.move: tuple = None # (y,x), choosen_piece
   
```
The player exploits one single function called `search_move`. 
Infact it checks if a move (complete with placing and choosing) is already computed. If not the player must use this function. Otherwise it will exploit the already computed move. This is a trick to call the function and compute the state once using results for both functions. Once the player's turn is over the move will be surely recomputed.

```py
def search_move(self, start_board, piece_to_play):

        possible_pieces: list = cook_status(board=start_board, 
                                    choosing=True,
                                    shuffle=True)['possible_pieces'] 

        possible_pieces.remove(piece_to_play)

        possible_new_states = cook_status(board=start_board, 
                                   selected_piece=piece_to_play, 
                                   my_test=True,
                                   shuffle=True)['future_states']

        # Try every combination of place-choice possible from this state
    
        # A test for "Dynamic" Depth
        # complexity = len(possible_new_states)*len(possible_pieces)
        #if complexity < 80:
           # self._MAX_DEPTH += 1

        for board, move in tqdm(possible_new_states, desc= f"Depth MAX = {self._MAX_DEPTH}"): 
            for p in tqdm(possible_pieces, leave=False):

                # Defining starting state
                root_state = MinMaxNode(board=board,
                                        choosen_piece= p,
                                        player= True,
                                        children= [])

                score = minimax(state=root_state, 
                                depth=self._MAX_DEPTH,
                                alpha=-99999,
                                beta=99999,
                                maximizing_player=True)

                if score > 0:
                    print("SEARCH went Good", move, p)
                    self.move = (move, p)
                    return
                
        #If minMax does not work out, try easy win and avoid defeat
        move, _ = try_easy_win(possible_new_states)
        piece, we_lost = avoid_easy_defeat(start_board, possible_pieces)
        print("SEARCH went Bad", move, piece)
        self.move = (move, piece)
        return

```
This function uses minmax to search for the next best state starting from the current one. From the state it finds, it extracts where to place the given piece, and what piece offer to the opponent. If no results can be computed satisfying the constraints, it will play like an HardCoded player.

The main functions of the player are then: 

```py
 def choose_piece(self) -> int:
        
        game = self.get_game()
        board = game.get_board_status()
        possible_pieces = cook_status(board=board,
                                      choosing=True)["possible_pieces"]

        candidate_piece, no_safe_pieces = avoid_easy_defeat(board, possible_pieces)

        if self._play_random or no_safe_pieces: 
            print(f"RANDOM PLAY CH or WE LOST {no_safe_pieces}", candidate_piece)
            return candidate_piece

        # It's the end of my turn, so:
        if self.move is not None:      # if there is a move loaded
            tmp_move = self.move       # save it
            self.move = None           # Delete the move
            print("Let chose: ", tmp_move[1], possible_pieces)  

            #TODO: Check if the move is a sure win for the opp
            # in that case try -> Avoid_easy_defeat
            # Isn't it spoiling the minmax approach?
            
            return tmp_move[1]  #return the move
    
        else: #if move is None 
            # This should be the first move so it can be easy to choose random...
            print("First Choice MOVE")
            return random.choice(possible_pieces)

```

And

```py
 def place_piece(self) -> tuple((int, int)):

        game = self.get_game()
        board = game.get_board_status()
        piece_to_place = game.get_selected_piece()
        possible_new_states = cook_status(board=board,
                                          selected_piece=piece_to_place,
                                          my_test=True,
                                          shuffle=True)["future_states"]

        # check for stop playing random
        self._play_random = False if self._turns_played_rnd >= self._MAX_RND else True

        candidate_move, is_winning = try_easy_win(possible_new_states)

        #if is_winning or self._play_random:
        if self._play_random:
            self._turns_played_rnd += 1
            print(f"RANDOM PLAY PL or IS_WINNING {is_winning}", candidate_move, piece_to_place)
            return candidate_move # (y,x) ??
        #print(possible_new_states)
        self.search_move(board, piece_to_place)
        
        print("Lets place: ", piece_to_place, "in",  self.move[0])
        print("Try easy Win says: ",candidate_move ,is_winning )
        return self.move[0]
        
```

### - Symmetries & Equivalences
I also considered using symmetries, such as flips and rotations, and then implementing Equivalences between different states, in order to greatly reduce the state space. The idea was to consider two state equivalent if both of them had in order:

- The same number of pieces
- The pieces configuration which differs only for rotation and/or flips
- The same graph of similarities of the pieces

(the idea of the graph of similarities was creating a graph for a state where the nodes are the position of a piece, and the edges are the number of shared features between each node) 

Unfortunately I couldn't implement this feature due to its intrinsic complexity, both implementative and computational, and for the limited time I had.

## Raw Code

Hardcoded Player

```py
import logging
import argparse
import random
import quarto
from utils import *

class HardCodedPlayer(quarto.Player):
    """Random player"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)

    def choose_piece(self) -> int:

        game = self.get_game()
        board = game.get_board_status()
        possible_pieces = cook_status(board=board,
                                      choosing=True)["possible_pieces"]

        candidate_piece, no_safe_pieces = avoid_easy_defeat(board, possible_pieces)

        return candidate_piece

    def place_piece(self) -> tuple((int, int)):

        game = self.get_game()
        board = game.get_board_status()
        piece_to_place = game.get_selected_piece()
        possible_new_states = cook_status(board=board,
                                          selected_piece=piece_to_place,
                                          my_test=True)["future_states"]

        candidate_move, is_winning = try_easy_win(possible_new_states)
            
        return candidate_move
       

```

double_minmax.py

```py

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


```

```py
from copy import deepcopy
import quarto
from utils import cook_status
from double_minmax import minmax_choice, minmax_place, try_easy_win, avoid_easy_defeat

class DoubleMinMax(quarto.Player):
    def __init__(self, quarto: quarto) -> None:
        """
        The player starts playing randomly, then at a specific point
        it starts to play using minmax.
        This should limit the amount of states to analyse, especially at the beginning

        Args:
            quarto (quarto): pass the game
        """

        super().__init__(quarto)
        self._play_random: bool = True
        self._turns_played_rnd: int = 0
        self._MAX_RND = 2
        self._MAX_DEPTH = 30

   
    def choose_piece(self) -> int:

        game = self.get_game()
        board = game.get_board_status()
        possible_pieces = cook_status(board=board,
                                      choosing=True)["possible_pieces"]

        candidate_piece, is_winning = avoid_easy_defeat(board, possible_pieces)

        # if is winning is True, there is no hope for us, unless the opponent plays randomly
        # so it can be useful immplement 'or is_winninng' in the following if-statement, 
        # and die with honor
        if self._play_random or is_winning: 
            print("RANDOM PLAY CH", candidate_piece)
            return candidate_piece

        for piece in possible_pieces:

            score = minmax_place(curr_state=(deepcopy(board), piece), 
                                is_maximizing=False, # it's up to the opponent to place
                                depth=self._MAX_DEPTH,
                                alpha=-100_000,
                                beta=100_000)

            # if we find a state in which we win when we choose this piece...
            if score > 0:   
                print("Found a choosing to WIN", piece)
                return piece
        
        print("Choose NADA ...", candidate_piece)
        return candidate_piece
            
        
    def place_piece(self) -> tuple((int, int)):

        game = self.get_game()
        board = game.get_board_status()
        piece_to_place = game.get_selected_piece()
        possible_new_states = cook_status(board=board,
                                          selected_piece=piece_to_place)["possible_new_states"]

        # check for stopping playing random
        self._play_random = False if self._turns_played_rnd >= self._MAX_RND else True

        candidate_move, is_winning  = try_easy_win(possible_new_states)

        if is_winning or self._play_random:
            self._turns_played_rnd += 1
            print("RANDOM PLAY PL", candidate_move)
            return candidate_move # (y,x) ??
        
        # Else MinMax
        for state, move in possible_new_states:

            score = minmax_choice(board=deepcopy(state), 
                                  is_maximizing=True, 
                                  depth=self._MAX_DEPTH,
                                  alpha=-100_000,
                                  beta=100_000)

            if score > 0:
               print("Found a placing to WIN", (move[1], move[0]) )
               return (move[1], move[0])
        
        print("Place NADA ...", candidate_move)
        return candidate_move
            

```
equivalence.py  (WIP)
```py

from numpy import rot90, flip, fliplr, flipud
import numpy as np


def flip_over_diag(M: np.ndarray, on_anti_diag: bool=False) -> np.ndarray:
    return rot90(fliplr(M)) if not on_anti_diag else rot90(flipud(M))

if  __name__== "__main__":

    # for test
    M = np.array([[0,1,2,3], [4,5,6,7], [8,9,10,11], [12,13,14,15]])

    print(np.linalg.eigvals(M) )

    M1 = flip_over_diag(M, on_anti_diag=True)

    print(np.linalg.eigvals(M1) )
```

single_minmax.py

```py
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

```

SingleMinMax.py

```py

import random
import quarto
from utils import cook_status
from utils import try_easy_win, avoid_easy_defeat
from single_minmax import MinMaxNode, minimax

from tqdm import tqdm 



class SingleMinMax(quarto.Player):
    def __init__(self, quarto: quarto) -> None:
        """
        The player starts plaing randomly, then at a specific point
        it starts to play using minmax.
        This should limit the amount of states to analyse

        Args:
            quarto (quarto): pass the game
            max_depth (int): max exploration depth in the tree
            pieces_left (int): number of pieces left to activate minmax
        """

        super().__init__(quarto)
        self._play_random: bool = True
        self._turns_played_rnd: int = 0
        self._MAX_RND = 2
        self._MAX_DEPTH = 3
        self.move: tuple = None # (y,x), choosen_piece
   
    def choose_piece(self) -> int:
        
        game = self.get_game()
        board = game.get_board_status()
        possible_pieces = cook_status(board=board,
                                      choosing=True)["possible_pieces"]

        candidate_piece, no_safe_pieces = avoid_easy_defeat(board, possible_pieces)

        if self._play_random or no_safe_pieces: 
            print(f"RANDOM PLAY CH or WE LOST {no_safe_pieces}", candidate_piece)
            return candidate_piece

        # It's the end of my turn, so:
        if self.move is not None:      # if there is a move loaded
            tmp_move = self.move       # save it
            self.move = None           # Delete the move
            print("Let chose: ", tmp_move[1], possible_pieces)  

            #TODO: Check if the move is a sure win for the opp
            # in that case try -> Avoid_easy_defeat
            # Isn't it spoiling the minmax approach?
            
            return tmp_move[1]  #return the move
    
        else: #if move is None 
            # This should be the first move so it can be easy to choose random...
            print("First Choice MOVE")
            return random.choice(possible_pieces)
        
        
    def place_piece(self) -> tuple((int, int)):

        game = self.get_game()
        board = game.get_board_status()
        piece_to_place = game.get_selected_piece()
        possible_new_states = cook_status(board=board,
                                          selected_piece=piece_to_place,
                                          my_test=True,
                                          shuffle=True)["future_states"]

        # check for stop playing random
        self._play_random = False if self._turns_played_rnd >= self._MAX_RND else True

        candidate_move, is_winning = try_easy_win(possible_new_states)

        #if is_winning or self._play_random:
        if self._play_random:
            self._turns_played_rnd += 1
            print(f"RANDOM PLAY PL or IS_WINNING {is_winning}", candidate_move, piece_to_place)
            return candidate_move # (y,x) ??
        #print(possible_new_states)
        self.search_move(board, piece_to_place)
        
        print("Lets place: ", piece_to_place, "in",  self.move[0])
        print("Try easy Win says: ",candidate_move ,is_winning )
        return self.move[0]
        

    def search_move(self, start_board, piece_to_play):

        possible_pieces: list = cook_status(board=start_board, 
                                    choosing=True,
                                    shuffle=True)['possible_pieces'] 

        possible_pieces.remove(piece_to_play)

        possible_new_states = cook_status(board=start_board, 
                                   selected_piece=piece_to_play, 
                                   my_test=True,
                                   shuffle=True)['future_states']

        # Try every combination of place-choice possible from this state
    
        # A test for "Dynamic" Depth
        # complexity = len(possible_new_states)*len(possible_pieces)
        #if complexity < 80:
           # self._MAX_DEPTH += 1

        for board, move in tqdm(possible_new_states, desc= f"Depth MAX = {self._MAX_DEPTH}"): 
            for p in tqdm(possible_pieces, leave=False):

                # Defining starting state
                root_state = MinMaxNode(board=board,
                                        choosen_piece= p,
                                        player= True,
                                        children= [])

                score = minimax(state=root_state, 
                                depth=self._MAX_DEPTH,
                                alpha=-99999,
                                beta=99999,
                                maximizing_player=True)

                if score > 0:
                    print("SEARCH went Good", move, p)
                    self.move = (move, p)
                    return
                
        #If minMax does not work out, try easy win and avoid defeat
        move, _ = try_easy_win(possible_new_states)
        piece, we_lost = avoid_easy_defeat(start_board, possible_pieces)
        print("SEARCH went Bad", move, piece)
        self.move = (move, piece)
        return

```

utils.py

```py
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

    # TODO: Importante: Fare il copy della board!!! x
    # assert choosing == True or (choosing == False and selected_piece != None and board != None), \
    # f"If the Agent role is to position a piece, the actual board and the \
    # chosen piece must be specified inside the '__cook_status' function"

    cooked = dict()
    
    # Role: Choosing a Piece
    # TODO: CHeck se funge + Check 
    # for i in range(16): 
    #   if i not in board:
    #       poss_pieces.append(i) 

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
            # for y in range(4):
            #     for x in range(4):
            #         if board[y][x] < 0:
            #             # y,x or  x,y ??? DONT TACCC
            #             cooked['legal_moves'].append((y,x)) # before (x,y, piece)

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

    # for elem in l:
    #     elem_bits = '{:04b}'.format(elem)
    #     bits_matrix.append(elem_bits)

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
            return  ((move[0],move[1]), True)  # y,x for bug(?) in the quarto class (?)

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
```

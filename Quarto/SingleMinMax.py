
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


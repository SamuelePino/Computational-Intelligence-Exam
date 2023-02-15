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
            return candidate_move
        
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
            

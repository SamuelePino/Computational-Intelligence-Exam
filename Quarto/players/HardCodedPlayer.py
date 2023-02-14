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
       
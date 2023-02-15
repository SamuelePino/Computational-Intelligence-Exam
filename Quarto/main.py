# Free for personal or classroom use; see 'LICENSE.md' for details.
# https://github.com/squillero/computational-intelligence

import logging
import argparse
import random
import quarto

from DoubleMinMax import DoubleMinMax
from delivered_player.SingleMinMax import SingleMinMax
from players.HardCodedPlayer import HardCodedPlayer

from players.RandomPlayer import RandomPlayer


def main():
    game = quarto.Quarto()
    game.set_players((SingleMinMax(game), HardCodedPlayer(game)))
    winner = game.run()
    logging.warning(f"main: Winner: player {winner}")
"""
def main():
    game = quarto.Quarto()
    game.set_players((RandomPlayer(game), RandomPlayer(game)))
    winner = game.run()
    logging.warning(f"main: Winner: player {winner}")
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase log verbosity')
    parser.add_argument('-d',
                        '--debug',
                        action='store_const',
                        dest='verbose',
                        const=2,
                        help='log debug messages (same as -vv)')
    args = parser.parse_args()

    if args.verbose == 0:
        logging.getLogger().setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        logging.getLogger().setLevel(level=logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(level=logging.DEBUG)

    main()
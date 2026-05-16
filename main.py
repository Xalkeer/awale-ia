import math

from awale import Awale
from player import HumanPlayer, StupidBot
from minMax import MinMaxBot
from game import Game
from mcts import MCTS


class MCTSAdapter:
    """Petit adaptateur pour rendre MCTS compatible avec Game.

    Game attend des joueurs qui exposent get_awale(), get_name(), get_number()
    et choose_move(valid_moves). MCTS fournit choose_move(awale) ; on
    enveloppe pour garder une référence partagée à l'Awale.
    """
    def __init__(self, player_id, awale, max_iterations=1000, max_time=1.0, c=math.sqrt(2)):
        self.number = player_id
        self.awale = awale
        self.mcts = MCTS(player_id=player_id, max_iterations=max_iterations, max_time=max_time, c=c)

    def get_number(self):
        return self.number

    def get_name(self):
        return f"MCTS(P{self.number})"

    def get_awale(self):
        return self.awale

    def choose_move(self, valid_moves):
        # Game passes valid_moves, but MCTS wants the full state
        return self.mcts.choose_move(self.awale)


def main():
    awale_game = Awale()
    p1 = MCTSAdapter(player_id=0, awale=awale_game, max_iterations=1000, max_time=1.0, c=math.sqrt(2))
    p2 = MinMaxBot(number=1, awale=awale_game, name="MinMax (Top)", max_depth=6)
    game = Game(p1, p2)
    game.start()


if __name__ == "__main__":
    main()

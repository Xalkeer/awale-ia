import random
from awale import Awale
from mcts import MCTS


class HumanPlayer:
    def __init__(self, number, awale, name=""):
        if number not in (0, 1):
            raise ValueError("Player number must be 0 or 1.")
        self.number = number
        self.awale = awale
        self.name = name or f"Human {number + 1}"
        self.pending_move = None

    def get_number(self):
        return self.number

    def get_name(self):
        return self.name

    def get_awale(self):
        return self.awale

    def set_move(self, hole):
        self.pending_move = hole

    def choose_move(self, valid_moves):
        move = self.pending_move
        if move in valid_moves:
            self.pending_move = None
            return move
        return None

    def __str__(self):
        return f"{self.name} (player {self.number + 1})"


class StupidBot:
    def __init__(self, number, awale, name=""):
        if number not in (0, 1):
            raise ValueError("Player number must be 0 or 1.")
        self.number = number
        self.awale = awale
        self.name = name or f"StupidBot {number + 1}"

    def get_number(self):
        return self.number

    def get_name(self):
        return self.name

    def get_awale(self):
        return self.awale

    def choose_move(self, valid_moves):
        if valid_moves:
            return random.choice(valid_moves)
        return None

    def __str__(self):
        return f"{self.name} (player {self.number + 1})"


class MCTSBot:
    def __init__(self, number, awale, name="",
                 max_iterations=500, max_time=None, c=None):
        if number not in (0, 1):
            raise ValueError("Player number must be 0 or 1.")
        self.number = number
        self.awale = awale
        self.name = name or f"MCTSBot {number + 1}"

        import math
        self._mcts = MCTS(
            player_id=number,
            max_iterations=max_iterations,
            max_time=max_time,
            c=c if c is not None else math.sqrt(2)
        )

    def get_number(self):
        return self.number

    def get_name(self):
        return self.name

    def get_awale(self):
        return self.awale

    def choose_move(self, valid_moves):
        if not valid_moves:
            return None
        return self._mcts.choose_move(self.awale)

    def __str__(self):
        return f"{self.name} (player {self.number + 1})"

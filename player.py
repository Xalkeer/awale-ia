import random
from awale import Awale


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

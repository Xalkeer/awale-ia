import random
from awale import Awale


class HumanPlayer:
    def __init__(self, number: int, awale: Awale, name: str = ""):
        if number not in (0, 1):
            raise ValueError("Player number must be 0 or 1.")
        self._number = number
        self._awale = awale
        self._name = name or f"Human {number + 1}"
        self._pending_move = None

    def get_number(self):
        return self._number

    def get_name(self):
        return self._name

    def get_awale(self):
        return self._awale

    def set_move(self, hole: int):
        self._pending_move = hole

    def choose_move(self, valid_moves: list) -> int:
        move = self._pending_move
        if move in valid_moves:
            self._pending_move = None
            return move
        return None

    def __str__(self):
        return f"{self._name} (player {self._number + 1})"


class StupidBot:
    def __init__(self, number: int, awale: Awale, name: str = ""):
        if number not in (0, 1):
            raise ValueError("Player number must be 0 or 1.")
        self._number = number
        self._awale = awale
        self._name = name or f"StupidBot {number + 1}"

    def get_number(self):
        return self._number

    def get_name(self):
        return self._name

    def get_awale(self):
        return self._awale

    def choose_move(self, valid_moves: list) -> int:
        if valid_moves:
            return random.choice(valid_moves)
        return None

    def __str__(self):
        return f"{self._name} (player {self._number + 1})"
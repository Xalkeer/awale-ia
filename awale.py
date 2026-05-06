class Awale:
    NB_HOLES = 12
    NB_HOLES_PER_PLAYER = 6
    INITIAL_SEEDS = 4

    def __init__(self):
        self._board = [self.INITIAL_SEEDS] * self.NB_HOLES
        self._captures = [0, 0]
        self._current_player = 0

    def get_board(self):
        return self._board[:]

    def get_captures(self):
        return self._captures[:]

    def get_current_player(self):
        return self._current_player

    def get_seeds_hole(self, index):
        return self._board[index]

    def get_score(self, player):
        return self._captures[player]

    def _player_holes(self, player):
        if player == 0:
            return list(range(0, 6))
        else:
            return list(range(6, 12))

    def _opponent(self, player):
        return 1 - player

    def _total_seeds_player(self, player):
        return sum(self._board[i] for i in self._player_holes(player))

    def valid_moves(self, player=None):
        if player is None:
            player = self._current_player

        opponent = self._opponent(player)
        holes = self._player_holes(player)

        candidates = [i for i in holes if self._board[i] > 0]

        if not candidates:
            return []

        if self._total_seeds_player(opponent) == 0:
            feeding_moves = [
                i for i in candidates
                if self._simulates_feeding(i, player)
            ]
            return feeding_moves if feeding_moves else candidates

        return candidates

    def _simulates_feeding(self, hole, player):
        opponent = self._opponent(player)
        opponent_holes = self._player_holes(opponent)

        temp_board = self._board[:]
        seeds = temp_board[hole]
        temp_board[hole] = 0
        pos = hole

        for _ in range(seeds):
            pos = (pos + 1) % self.NB_HOLES
            if pos == hole:
                pos = (pos + 1) % self.NB_HOLES
            temp_board[pos] += 1

        return any(temp_board[i] > 0 for i in opponent_holes)

    def play(self, hole):
        if hole not in self.valid_moves():
            return False

        final_hole = self._sow(hole)
        self._capture(final_hole)

        self._current_player = self._opponent(self._current_player)
        return True

    def _sow(self, hole):
        seeds = self._board[hole]
        self._board[hole] = 0
        pos = hole

        for _ in range(seeds):
            pos = (pos + 1) % self.NB_HOLES
            if pos == hole:
                pos = (pos + 1) % self.NB_HOLES
            self._board[pos] += 1

        return pos

    def _capture(self, final_pos):
        player = self._current_player
        opponent = self._opponent(player)
        opponent_holes = set(self._player_holes(opponent))

        if final_pos not in opponent_holes:
            return

        to_capture = []
        pos = final_pos

        while pos in opponent_holes and self._board[pos] in (2, 3):
            to_capture.append(pos)
            pos = (pos - 1) % self.NB_HOLES

        if not to_capture:
            return

        total_opponent_seeds = sum(self._board[i] for i in opponent_holes)
        targeted_seeds = sum(self._board[i] for i in to_capture)

        if targeted_seeds == total_opponent_seeds:
            return

        for p in to_capture:
            self._captures[player] += self._board[p]
            self._board[p] = 0

    def is_finished(self):
        if self._captures[0] > 24 or self._captures[1] > 24:
            return True
        if self._captures[0] == 24 and self._captures[1] == 24:
            return True
        if not self.valid_moves():
            return True
        if sum(self._board) <= 6:
            return True
        return False

    def winner(self):
        if not self.is_finished():
            return None

        scores = self._captures[:]
        for player in (0, 1):
            for i in self._player_holes(player):
                scores[player] += self._board[i]

        if scores[0] > scores[1]:
            return 0
        elif scores[1] > scores[0]:
            return 1
        else:
            return -1

    def final_scores(self):
        scores = self._captures[:]
        for player in (0, 1):
            for i in self._player_holes(player):
                scores[player] += self._board[i]
        return scores

    def copy(self):
        new_game = Awale.__new__(Awale)
        new_game._board = self._board[:]
        new_game._captures = self._captures[:]
        new_game._current_player = self._current_player
        return new_game

    def __str__(self):
        p = self._board
        line1 = "  ".join(f"{p[i]:2d}" for i in range(11, 5, -1))
        line2 = "  ".join(f"{p[i]:2d}" for i in range(0, 6))
        sep = "-" * 35
        return (
            f"Player 2 [{self._captures[1]:2d}] : {line1}\n"
            f"{sep}\n"
            f"Player 1 [{self._captures[0]:2d}] : {line2}"
        )
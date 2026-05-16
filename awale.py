class Awale:
    NB_HOLES = 12
    NB_HOLES_PER_PLAYER = 6
    INITIAL_SEEDS = 4

    def __init__(self):
        self.board = [self.INITIAL_SEEDS] * self.NB_HOLES
        self.captures = [0, 0]
        self.current_player = 0

    def get_board(self):
        return self.board[:]

    def get_captures(self):
        return self.captures[:]

    def get_current_player(self):
        return self.current_player

    def get_seeds_hole(self, index):
        return self.board[index]

    def get_score(self, player):
        return self.captures[player]

    def player_holes(self, player):
        if player == 0:
            return list(range(0, 6))
        else:
            return list(range(6, 12))

    def opponent(self, player):
        return 1 - player

    def total_seeds_player(self, player):
        return sum(self.board[i] for i in self.player_holes(player))

    def valid_moves(self, player=None):
        if player is None:
            player = self.current_player

        opponent = self.opponent(player)
        holes = self.player_holes(player)

        candidates = [i for i in holes if self.board[i] > 0]

        if not candidates:
            return []

        if self.total_seeds_player(opponent) == 0:
            feeding_moves = [
                i for i in candidates
                if self.simulates_feeding(i, player)
            ]
            return feeding_moves if feeding_moves else candidates

        return candidates

    def simulates_feeding(self, hole, player):
        opponent = self.opponent(player)
        opponent_holes = self.player_holes(opponent)

        temp_board = self.board[:]
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

        final_hole = self.sow(hole)
        self.capture(final_hole)

        self.current_player = self.opponent(self.current_player)
        return True


    def sow(self, hole):
        seeds = self.board[hole]
        self.board[hole] = 0
        pos = hole

        for _ in range(seeds):
            pos = (pos + 1) % self.NB_HOLES
            if pos == hole:
                pos = (pos + 1) % self.NB_HOLES
            self.board[pos] += 1

        return pos

    def capture(self, final_pos):
        player = self.current_player
        opponent = self.opponent(player)
        opponent_holes = set(self.player_holes(opponent))

        if final_pos not in opponent_holes:
            return

        to_capture = []
        pos = final_pos

        while pos in opponent_holes and self.board[pos] in (2, 3):
            to_capture.append(pos)
            pos = (pos - 1) % self.NB_HOLES

        if not to_capture:
            return

        total_opponent_seeds = sum(self.board[i] for i in opponent_holes)
        targeted_seeds = sum(self.board[i] for i in to_capture)

        if targeted_seeds == total_opponent_seeds:
            return

        for p in to_capture:
            self.captures[player] += self.board[p]
            self.board[p] = 0

    def is_finished(self):
        if self.captures[0] > 24 or self.captures[1] > 24:
            return True
        if self.captures[0] == 24 and self.captures[1] == 24:
            return True
        if not self.valid_moves():
            return True
        if sum(self.board) <= 6:
            return True
        return False

    def winner(self):
        if not self.is_finished():
            return None

        scores = self.captures[:]
        for player in (0, 1):
            for i in self.player_holes(player):
                scores[player] += self.board[i]

        if scores[0] > scores[1]:
            return 0
        elif scores[1] > scores[0]:
            return 1
        else:
            return -1

    def final_scores(self):
        scores = self.captures[:]
        for player in (0, 1):
            for i in self.player_holes(player):
                scores[player] += self.board[i]
        return scores

    def copy(self):
        new_game = Awale.__new__(Awale)
        new_game.board = self.board[:]
        new_game.captures = self.captures[:]
        new_game.current_player = self.current_player
        return new_game

    def __str__(self):
        p = self.board
        line1 = "  ".join(f"{p[i]:2d}" for i in range(11, 5, -1))
        line2 = "  ".join(f"{p[i]:2d}" for i in range(0, 6))
        sep = "-" * 35
        return (
            f"Player 2 [{self.captures[1]:2d}] : {line1}\n"
            f"{sep}\n"
            f"Player 1 [{self.captures[0]:2d}] : {line2}"
        )

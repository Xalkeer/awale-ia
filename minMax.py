from cmath import inf


class MinMax:
    def __init__(self, number, awale, name="", depth=4):
        if number not in (0, 1):
            raise ValueError("Player number must be 0 or 1.")
        self.number = number
        self.awale = awale
        self.name = name or f"MinMaxBot {number + 1}"
        self.depth = depth

    def heuristic_material(self, game_state):
        score_ia = game_state.get_score(self.number)
        score_adv = game_state.get_score(1 - self.number)
        if score_ia > 24: return inf
        if score_adv > 24: return -inf
        return score_ia - score_adv

    def minimax(self, game_state, depth, maximizing_player):
        if depth == 0 or game_state.is_finished():
            return self.heuristic_material(game_state), None

        valid_moves = game_state.valid_moves()
        if maximizing_player:
            max_eval = -inf
            best_move = None
            for move in valid_moves:
                new_state = game_state
                eval, _ = self.minimax(new_state, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = inf
            best_move = None
            for move in valid_moves:
                new_state = self.simulate_move(game_state, move)
                eval, _ = self.minimax(new_state, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move
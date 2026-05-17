import copy


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
        if score_ia > 24: return float('inf')
        if score_adv > 24: return -float('inf')
        return score_ia - score_adv

    def heuristic_strategic(self, game_state):
        score = self.heuristic_material(game_state)
        mes_trous = game_state.player_holes(self.number)
        trous_adv = game_state.player_holes(1 - self.number)
        board = game_state.get_board()
        for i in mes_trous:
            if board[i] in (1, 2):
                score -= 0.5
        for i in trous_adv:
            if board[i] in (1, 2):
                score += 0.5

        return score

    def get_best_move(self):
        val, move = self.minimax(
            self.awale,
            self.depth,
            -float('inf'),
            float('inf'),
            True
        )
        return move

    def minimax(self, game_state, depth, alpha, beta, maximizing_player):
        if depth == 0 or game_state.is_finished():
            return self.heuristic_strategic(game_state), None
        moves = game_state.valid_moves()
        if not moves:
            return self.heuristic_strategic(game_state), None
        best_move = moves[0]
        if maximizing_player:
            max_eval = -float('inf')
            for move in moves:
                new_state = game_state.copy()
                new_state.play(move)
                eval_score, _ = self.minimax(new_state, depth - 1, alpha, beta, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    return max_eval, best_move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in moves:
                new_state = game_state.copy()
                new_state.play(move)
                eval_score, _ = self.minimax(new_state, depth - 1, alpha, beta, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    return min_eval, best_move
            return min_eval, best_move
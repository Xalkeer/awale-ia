from math import inf
import time


class MinMaxBot:
    def __init__(self, number, awale, name="", max_depth=6, heuristic="default", pruning=True):
        self.number = number
        self.awale = awale
        self.name = name or f"MinMaxBot {number + 1}"
        self.max_depth = max_depth
        self.heuristic = heuristic
        self.use_pruning = pruning

        self.start_time = None

    def get_number(self):
        return self.number

    def get_name(self):
        return self.name

    def get_awale(self):
        return self.awale

    def choose_move(self, valid_moves):
        if not valid_moves:
            return None

        # utile au statistique
        self.start_time = time.perf_counter()

        ordered_moves = self.order_moves(self.awale, valid_moves, self.number)
        best_move = ordered_moves[0]
        best_value = -inf

        for move in ordered_moves:

            next_game = self.awale.copy()
            next_game.play(move)
            next_player = next_game.get_current_player()

            value, _ = self.play_minmax(next_game,next_player,self.max_depth - 1,-inf,inf)

            if value > best_value:
                best_value = value
                best_move = move

        return best_move

    def play_minmax(self, game, player, depth, alpha=-inf, beta=inf):

        if self.is_terminal(game) or depth == 0:
            return self.evaluateHeuristic(game), None

        valid_moves = game.valid_moves(player)
        if not valid_moves:
            return self.evaluateHeuristic(game), None

        ordered_moves = self.order_moves(game, valid_moves, player)

        if player == self.number:
            best_value = -inf
            best_move = None

            for move in ordered_moves:
                child = game.copy()
                child.play(move)
                value, _ = self.play_minmax(child, child.get_current_player(), depth - 1, alpha, beta)

                if value > best_value:
                    best_value = value
                    best_move = move

                if self.use_pruning:
                    alpha = max(alpha, best_value)
                    if alpha >= beta:
                        break

            result = (best_value, best_move)
        else:
            best_value = inf
            best_move = None

            for move in ordered_moves:
                child = game.copy()
                child.play(move)
                value, _ = self.play_minmax(child, child.get_current_player(), depth - 1, alpha, beta)

                if value < best_value:
                    best_value = value
                    best_move = move

                if self.use_pruning:
                    beta = min(beta, best_value)
                    if alpha >= beta:
                        break

            result = (best_value, best_move)

        return result

    def is_terminal(self, game):
        return game.is_finished()


    def order_moves(self, game, moves, player):
        scored_moves = []
        for move in moves:
            child = game.copy()
            child.play(move)
            scored_moves.append((self.evaluateHeuristic(child), move))

        reverse = player == self.number
        scored_moves.sort(key=lambda item: item[0], reverse=reverse)
        return [move for _, move in scored_moves]

    def evaluateHeuristic(self, game):
        if self.heuristic == "lookahead":
            return self.secondHeuristic(game)
        return self.firstHeurtisitc(game)


    # Heuristic simple : On valorise uniquement le fait de capturer une graine
    def firstHeurtisitc(self, game):
        player = self.number
        opponent = 1 - player

        if game.is_finished():
            return self.final_score(game)

        captures_diff = game.get_score(player) - game.get_score(opponent)
        seeds_diff = game.total_seeds_player(player) - game.total_seeds_player(opponent)

        return captures_diff * 10.0 + seeds_diff * 1.0


    # Joue en fonction du prochain coup jouer de l'adversaire, plus forte mais prends plus de temps
    # On prend d'abord le fait de capturer ou non des graines en x20 étant donné que c'est le plus important
    # Ensuite on check le nombre de coup possible, ça reste important mais pas autant que le précédent
    # Et en dernier on check le nombre de graine restant sur le plateau
    def secondHeuristic(self, game):
        player = self.number
        opponent = 1 - player

        if game.is_finished():
            return self.final_score(game)

        best_net = -inf

        for move in game.valid_moves(player):
            child = game.copy()
            before_player = child.get_score(player)
            child.play(move)
            after_player = child.get_score(player)

            opp_turn = child.get_current_player()
            opp_moves = child.valid_moves(opp_turn)
            max_opp_gain = 0
            for om in opp_moves:
                opp_child = child.copy()
                before_opp = opp_child.get_score(opponent)
                opp_child.play(om)
                gain = opp_child.get_score(opponent) - before_opp
                if gain > max_opp_gain:
                    max_opp_gain = gain

            net = (after_player - before_player) - max_opp_gain
            if net > best_net:
                best_net = net

        if best_net == -inf:
            best_net = 0

        mobility = len(game.valid_moves(player)) - len(game.valid_moves(opponent))
        seeds_balance = game.total_seeds_player(player) - game.total_seeds_player(opponent)

        return best_net * 20.0 + mobility * 2.0 + seeds_balance * 1.0


    def final_score(self, game):
        scores = game.final_scores()
        player = self.number
        opponent = 1 - player

        if scores[player] > scores[opponent]:
            return 10000 + (scores[player] - scores[opponent])
        if scores[player] < scores[opponent]:
            return -10000 + (scores[player] - scores[opponent])
        return 0

    def elapsed_time(self):
        if self.start_time is None:
            return 0.0
        return time.perf_counter() - self.start_time

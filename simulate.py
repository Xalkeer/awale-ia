import time
import statistics
import random
from awale import Awale
from player import StupidBot
from minMax import MinMaxBot
from mcts import MCTS


def simulate(n_games, player0_type, player1_type, max_depth=6, mcts_iterations=500, verbose=False, seed=None):
    """Lance des simulations de parties."""

    if seed is not None:
        random.seed(seed)

    stats = {
        "wins": {0: 0, 1: 0, -1: 0},
        "game_times": [],
        "moves_per_game": [],
        "choose_time": {0: [], 1: []},
    }

    for gi in range(1, n_games + 1):
        aw = Awale()

        # Créer les joueurs
        if player0_type == "stupid":
            p0 = StupidBot(0, aw, name="StupidBot(P0)")
        elif player0_type == "minmax":
            p0 = MinMaxBot(0, aw, name="MinMax(P0)", max_depth=max_depth)
        elif player0_type == "mcts":
            p0 = MCTS(player_id=0, max_iterations=mcts_iterations)
            p0.awale = aw

        if player1_type == "stupid":
            p1 = StupidBot(1, aw, name="StupidBot(P1)")
        elif player1_type == "minmax":
            p1 = MinMaxBot(1, aw, name="MinMax(P1)", max_depth=max_depth)
        elif player1_type == "mcts":
            p1 = MCTS(player_id=1, max_iterations=mcts_iterations)
            p1.awale = aw

        players = {0: p0, 1: p1}

        game_start = time.perf_counter()
        move_count = 0
        choose_time_game = {0: 0.0, 1: 0.0}

        # Jouer la partie
        while not aw.is_finished():
            current_player = aw.get_current_player()
            player = players[current_player]
            valid_moves = aw.valid_moves()

            if not valid_moves:
                break

            # Mesurer le temps
            t0 = time.perf_counter()

            if isinstance(player, MCTS):
                move = player.choose_move(aw)
            else:
                move = player.choose_move(valid_moves)

            t1 = time.perf_counter()

            choose_time_game[current_player] += (t1 - t0)

            # Jouer le coup
            if move is not None and aw.play(move):
                move_count += 1

        game_end = time.perf_counter()
        duration = game_end - game_start

        # Résultats
        winner = aw.winner()
        stats["wins"][winner] += 1
        stats["game_times"].append(duration)
        stats["moves_per_game"].append(move_count)
        stats["choose_time"][0].append(choose_time_game[0])
        stats["choose_time"][1].append(choose_time_game[1])

        # Afficher le résultat de la partie en temps réel (toujours)
        print(f"Game {gi:3d}: winner={winner:2d}, moves={move_count:3d}, "
              f"time={duration:.3f}s, p0_time={choose_time_game[0]:.3f}s, p1_time={choose_time_game[1]:.3f}s")

    # Résumé
    avg_time = statistics.mean(stats["game_times"]) if stats["game_times"] else 0.0
    median_time = statistics.median(stats["game_times"]) if stats["game_times"] else 0.0
    avg_moves = statistics.mean(stats["moves_per_game"]) if stats["moves_per_game"] else 0.0

    print("\n" + "="*60)
    print("SIMULATION REPORT")
    print("="*60)
    print(f"Total games:        {n_games}")
    print(f"\n{player0_type}(P0): {stats['wins'][0]} wins")
    print(f"{player1_type}(P1): {stats['wins'][1]} wins")
    print(f"Draws:              {stats['wins'][-1]}")
    print(f"\nAverage game time:  {avg_time:.3f}s (median: {median_time:.3f}s)")
    print(f"Average moves/game: {avg_moves:.2f}")
    print(f"\nThink times:")
    print(f"  {player0_type}(P0): {sum(stats['choose_time'][0]):.3f}s total")
    print(f"  {player1_type}(P1): {sum(stats['choose_time'][1]):.3f}s total")
    print("="*60)


def main():
    n_games = 10
    # Soit mcts,minmax,stupid,human
    player0_type = "stupid"
    player1_type = "minmax"
    max_depth = 6
    mcts_iterations = 500
    verbose = False
    seed = None

    simulate(n_games=n_games,
             player0_type=player0_type,
             player1_type=player1_type,
             max_depth=max_depth,
             mcts_iterations=mcts_iterations,
             verbose=verbose,
             seed=seed)


if __name__ == "__main__":
    main()



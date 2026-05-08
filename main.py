from awale import Awale
from player import StupidBot, HumanPlayer, MCTSBot
from game import Game


def main():
    awale_game = Awale()
    p1 = StupidBot(number=0, awale=awale_game, name="Stupid Bot")
    p2 = MCTSBot(number=1, awale=awale_game, name="MCTS", max_iterations=500)
    game = Game(p1, p2)
    game.start()


if __name__ == "__main__":
    main()
from awale import Awale
from player import StupidBot, HumanPlayer
from game import Game


def main():
    awale_game = Awale()
    p1 = HumanPlayer(number=0, awale=awale_game, name="R2D2 (Bottom)")
    p2 = StupidBot(number=1, awale=awale_game, name="C3PO (Top)")
    game = Game(p1, p2)
    game.start()


if __name__ == "__main__":
    main()
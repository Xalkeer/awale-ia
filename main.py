from awale import Awale
from player import StupidBot
from game import Game


def main():
    awale_game = Awale()
    bot1 = StupidBot(number=0, awale=awale_game, name="R2D2 (Bottom)")
    bot2 = StupidBot(number=1, awale=awale_game, name="C3PO (Top)")
    game = Game(bot1, bot2)
    game.start()


if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-


from game import Game
from sdl import SDL
#from level import Level


class QuanteeTheGame(Game):
    """QuanteeTheGame() -> our game"""

    def __init__(self):

        engine = SDL("Quantee", (640, 480))

        super(QuanteeTheGame, self).__init__(engine, None)

if __name__ == '__main__':
    game = QuanteeTheGame()
    game.run()

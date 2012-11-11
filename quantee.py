# -*- coding: utf-8 -*-

import pygame

from game import Game
from sdl import SDL, EventManager


class DumbManager(EventManager):
    """DumbManager() -> a dumb EventManager

    It allows for the presence of QUIT and NOEVENT pygame events and passes
    them on unmodified.
    """

    __allowed = [
            pygame.QUIT,
            pygame.NOEVENT]

    def transform(self, raw_event):
        """DM.transform(raw_event) -> raw_event

        Performs no transformations.
        """

        return raw_event


class QuanteeTheGame(Game):
    """QuanteeTheGame() -> our game"""

    def __init__(self):

        engine = SDL("Quantee", (640, 480), DumbManager())

        super(QuanteeTheGame, self).__init__(engine, None)


if __name__ == '__main__':
    game = QuanteeTheGame()
    game.run()

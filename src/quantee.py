# -*- coding: utf-8 -*-

import pygame

from game import Game
from sdl import SDL, EventManager

from level import Level
from stage import Stage
from ender import Ender

from cam import StaticCam
from boxes import Box


class DumbEnder(Ender):
    """DumbEnder() -> a dumb Ender

    Ends on a pygame.QUIT event and returns None as the next Level.
    """

    def done(self, dt, event, stage):

        print dt, event

        if event.type == pygame.QUIT:

            return True

        return False

    def next_level(self):

        return None


class DumbLevel(Level):
    """DumbLevel() -> a dumb Level

    It is empty and will end only on a QUIT event, and end the game
    alltogether.
    """

    def __init__(self):

        cam = StaticCam(Box(0, 0, 640, 480))
        stage = Stage((0, 0), ['no'], 'no')

        super(DumbLevel, self).__init__(cam, stage, DumbEnder())


class DumbManager(EventManager):
    """DumbManager() -> a dumb EventManager

    It allows for the presence of QUIT and NOEVENT pygame events and passes
    them on unmodified.
    """

    __allowed = [
            pygame.QUIT,
            pygame.NOEVENT]

    @property
    def allowed(self):
        """DM.allowed -> list of allowed PyGame event types

        Contains pygame.QUIT and pygame.NOEVENT.
        """

        return self.__allowed

    def transform(self, raw_event):
        """DM.transform(raw_event) -> raw_event

        Performs no transformations.
        """

        return raw_event


class QuanteeTheGame(Game):
    """QuanteeTheGame() -> our game"""

    def __init__(self):

        engine = SDL("Quantee", (640, 480), DumbManager())

        init_level = DumbLevel()

        super(QuanteeTheGame, self).__init__(engine, init_level)


if __name__ == '__main__':
    game = QuanteeTheGame()
    game.run()
